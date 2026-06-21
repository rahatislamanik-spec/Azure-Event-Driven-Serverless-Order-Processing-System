import azure.functions as func
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from azure.storage.queue import QueueClient
from azure.data.tables import TableServiceClient
from azure.communication.email import EmailClient

app = func.FunctionApp()


# =============================================================================
# submit_order — HTTP Trigger
# =============================================================================

@app.route(route="submit_order", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def submit_order(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("submit_order function triggered.")

    # ---- Parse JSON body ----
    try:
        order = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"status": "error", "message": "Invalid JSON body."}),
            status_code=400,
            mimetype="application/json"
        )

    # ---- Validate required fields (matches the real frontend form) ----
    required_fields = [
        "firstName",
        "lastName",
        "email",
        "phone",
        "deliveryAddress",
        "laptop",
        "quantity"
    ]
    missing_fields = [field for field in required_fields if not order.get(field) and order.get(field) != 0]

    if missing_fields:
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Missing required fields.",
                "missingFields": missing_fields
            }),
            status_code=400,
            mimetype="application/json"
        )

    # ---- Basic email format check ----
    email = order["email"]
    if "@" not in email or "." not in email.split("@")[-1]:
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Invalid email format."
            }),
            status_code=400,
            mimetype="application/json"
        )

    # ---- Quantity must be a positive integer ----
    try:
        quantity = int(order["quantity"])
        if quantity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Quantity must be a positive whole number."
            }),
            status_code=400,
            mimetype="application/json"
        )

    # ---- Derive business-friendly fields from raw frontend fields ----
    first_name = order["firstName"].strip()
    last_name = order["lastName"].strip()
    customer_name = f"{first_name} {last_name}".strip()
    product = order["laptop"]

    order_id = str(uuid.uuid4())

    # ---- Build the normalized queue message ----
    # Keeps both the raw frontend fields AND derived fields, so downstream
    # functions (validate_order, log_to_table, send_confirmation_email) have
    # clean fields to work with while the original submission is preserved.
    queue_message = {
        "orderId": order_id,
        "customerName": customer_name,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": order["phone"],
        "deliveryAddress": order["deliveryAddress"],
        "product": product,
        "laptop": product,
        "quantity": quantity,
        "status": "submitted",
        "submittedAt": datetime.now(timezone.utc).isoformat()
    }

    # ---- Connect to Azure Storage Queue ----
    connection_string = os.environ.get("AzureWebJobsStorage")

    if not connection_string:
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "AzureWebJobsStorage connection string is not configured."
            }),
            status_code=500,
            mimetype="application/json"
        )

    try:
        queue_client = QueueClient.from_connection_string(
            conn_str=connection_string,
            queue_name="orders-incoming"
        )
        queue_client.send_message(json.dumps(queue_message))
    except Exception as e:
        logging.error(f"Failed to send message to orders-incoming queue: {e}")
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Failed to submit order. Please try again."
            }),
            status_code=500,
            mimetype="application/json"
        )

    logging.info(f"Order {order_id} submitted to orders-incoming queue.")

    return func.HttpResponse(
        json.dumps({
            "status": "accepted",
            "message": "Order submitted successfully.",
            "orderId": order_id
        }),
        status_code=202,
        mimetype="application/json"
    )


# =============================================================================
# validate_order — Queue Trigger
# =============================================================================

def get_queue_client(queue_name: str) -> QueueClient:
    connection_string = os.environ["AzureWebJobsStorage"]
    return QueueClient.from_connection_string(
        conn_str=connection_string,
        queue_name=queue_name
    )


def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


@app.queue_trigger(
    arg_name="msg",
    queue_name="orders-incoming",
    connection="AzureWebJobsStorage"
)
def validate_order(msg: func.QueueMessage) -> None:
    logging.info("validate_order function triggered.")

    try:
        order = json.loads(msg.get_body().decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        logging.error(f"Failed to parse queue message as JSON: {e}")
        # Can't even parse it — push the raw body to orders-invalid for review
        try:
            invalid_client = get_queue_client("orders-invalid")
            invalid_client.send_message(json.dumps({
                "error": "Malformed message — could not parse JSON",
                "rawBody": msg.get_body().decode("utf-8", errors="replace")
            }))
        except Exception as inner_e:
            logging.error(f"Failed to route malformed message to orders-invalid: {inner_e}")
        return

    order_id = order.get("orderId", "UNKNOWN")
    validation_errors = []

    # ---- Re-validate required fields ----
    required_fields = [
        "orderId",
        "customerName",
        "firstName",
        "lastName",
        "email",
        "phone",
        "deliveryAddress",
        "product",
        "laptop",
        "quantity"
    ]
    missing_fields = [field for field in required_fields if not order.get(field) and order.get(field) != 0]
    if missing_fields:
        validation_errors.append(f"Missing required fields: {', '.join(missing_fields)}")

    # ---- Validate email format ----
    email = order.get("email", "")
    if email and not is_valid_email(email):
        validation_errors.append(f"Invalid email format: {email}")

    # ---- Validate quantity ----
    quantity = order.get("quantity")
    if quantity is not None:
        try:
            quantity_int = int(quantity)
            if quantity_int <= 0:
                validation_errors.append("Quantity must be greater than zero.")
        except (ValueError, TypeError):
            validation_errors.append("Quantity must be a whole number.")

    # ---- Route based on field validation result ----
    if validation_errors:
        logging.warning(f"Order {order_id} failed validation: {validation_errors}")
        invalid_payload = {
            **order,
            "status": "invalid",
            "validationErrors": validation_errors
        }
        try:
            invalid_client = get_queue_client("orders-invalid")
            invalid_client.send_message(json.dumps(invalid_payload))
            logging.info(f"Order {order_id} routed to orders-invalid queue.")
        except Exception as e:
            logging.error(f"Failed to route order {order_id} to orders-invalid: {e}")
        return

    # ---- Check inventory stock for the requested laptop ----
    laptop_name = order.get("laptop", "")
    requested_quantity = int(order.get("quantity", 0))

    connection_string = os.environ.get("AzureWebJobsStorage")
    table_service = TableServiceClient.from_connection_string(connection_string)
    inventory_table = table_service.get_table_client(table_name="LaptopInventory")

    try:
        inventory_entity = inventory_table.get_entity(
            partition_key="inventory",
            row_key=laptop_name
        )
        available_stock = inventory_entity.get("stockCount", 0)
    except Exception as e:
        logging.error(f"Could not find inventory record for '{laptop_name}': {e}")
        available_stock = 0

    if available_stock < requested_quantity:
        logging.warning(
            f"Order {order_id} rejected — insufficient stock for '{laptop_name}'. "
            f"Requested: {requested_quantity}, Available: {available_stock}"
        )
        invalid_payload = {
            **order,
            "status": "invalid",
            "validationErrors": [
                f"Insufficient stock for '{laptop_name}'. "
                f"Requested {requested_quantity}, only {available_stock} available."
            ]
        }
        try:
            invalid_client = get_queue_client("orders-invalid")
            invalid_client.send_message(json.dumps(invalid_payload))
            logging.info(f"Order {order_id} routed to orders-invalid queue (insufficient stock).")
        except Exception as e:
            logging.error(f"Failed to route order {order_id} to orders-invalid: {e}")
        return

    # ---- Stock is sufficient: decrement inventory ----
    try:
        inventory_entity["stockCount"] = available_stock - requested_quantity
        inventory_table.update_entity(mode="merge", entity=inventory_entity)
        logging.info(
            f"Inventory updated for '{laptop_name}': "
            f"{available_stock} -> {available_stock - requested_quantity}"
        )
    except Exception as e:
        # Log the failure but do not block the order — inventory drift is
        # preferable to losing a valid, already-accepted customer order.
        logging.error(f"Failed to decrement inventory for '{laptop_name}': {e}")

    # ---- Valid order: fan out to orders-to-email AND orders-to-log ----
    valid_payload = {
        **order,
        "status": "validated"
    }

    fan_out_failures = []

    try:
        email_client = get_queue_client("orders-to-email")
        email_client.send_message(json.dumps(valid_payload))
        logging.info(f"Order {order_id} sent to orders-to-email queue.")
    except Exception as e:
        logging.error(f"Failed to send order {order_id} to orders-to-email: {e}")
        fan_out_failures.append("orders-to-email")

    try:
        log_client = get_queue_client("orders-to-log")
        log_client.send_message(json.dumps(valid_payload))
        logging.info(f"Order {order_id} sent to orders-to-log queue.")
    except Exception as e:
        logging.error(f"Failed to send order {order_id} to orders-to-log: {e}")
        fan_out_failures.append("orders-to-log")

    if fan_out_failures:
        logging.error(
            f"Order {order_id} validated but failed to fan out to: {', '.join(fan_out_failures)}"
        )
    else:
        logging.info(f"Order {order_id} successfully validated and fanned out.")


# =============================================================================
# log_to_table — Queue Trigger
# =============================================================================

@app.queue_trigger(
    arg_name="msg",
    queue_name="orders-to-log",
    connection="AzureWebJobsStorage"
)
def log_to_table(msg: func.QueueMessage) -> None:
    logging.info("log_to_table function triggered.")

    try:
        order = json.loads(msg.get_body().decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        logging.error(f"Failed to parse queue message as JSON: {e}")
        return

    order_id = order.get("orderId", "UNKNOWN")

    connection_string = os.environ.get("AzureWebJobsStorage")
    if not connection_string:
        logging.error("AzureWebJobsStorage connection string is not configured.")
        return

    try:
        table_service = TableServiceClient.from_connection_string(connection_string)
        table_client = table_service.get_table_client(table_name="Orders")

        # Azure Table Storage requires PartitionKey and RowKey on every entity.
        # PartitionKey groups related rows together (using a fixed value here
        # since order volume in this project is low); RowKey must be unique
        # within a partition, so the order's own UUID is used.
        entity = {
            "PartitionKey": "orders",
            "RowKey": order_id,
            "customerName": order.get("customerName", ""),
            "firstName": order.get("firstName", ""),
            "lastName": order.get("lastName", ""),
            "email": order.get("email", ""),
            "phone": order.get("phone", ""),
            "deliveryAddress": order.get("deliveryAddress", ""),
            "product": order.get("product", ""),
            "quantity": order.get("quantity", 0),
            "status": order.get("status", ""),
            "submittedAt": order.get("submittedAt", "")
        }

        table_client.create_entity(entity=entity)
        logging.info(f"Order {order_id} successfully logged to Orders table.")

    except Exception as e:
        logging.error(f"Failed to log order {order_id} to Table Storage: {e}")


# =============================================================================
# send_confirmation_email — Queue Trigger
# =============================================================================

@app.queue_trigger(
    arg_name="msg",
    queue_name="orders-to-email",
    connection="AzureWebJobsStorage"
)
def send_confirmation_email(msg: func.QueueMessage) -> None:
    logging.info("send_confirmation_email function triggered.")

    try:
        order = json.loads(msg.get_body().decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        logging.error(f"Failed to parse queue message as JSON: {e}")
        return

    order_id = order.get("orderId", "UNKNOWN")
    recipient_email = order.get("email")

    if not recipient_email:
        logging.error(f"Order {order_id} has no email address — cannot send confirmation.")
        return

    connection_string = os.environ.get("ACS_CONNECTION_STRING")
    if not connection_string:
        logging.error("ACS_CONNECTION_STRING is not configured.")
        return

    # The Azure-managed sender domain — every Email Communication Service
    # using "AzureManagedDomain" gets a unique, pre-verified subdomain like
    # this one (no custom DNS setup or verification wait required).
    sender_address = "DoNotReply@7aeee3c2-241a-4930-ac4c-9968c4d91b42.azurecomm.net"

    customer_name = order.get("customerName", "Customer")
    product = order.get("product", "your laptop")
    quantity = order.get("quantity", 1)

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #1f2933;">
        <h2 style="color: #0078D4;">Order Confirmed</h2>
        <p>Hi {customer_name},</p>
        <p>Thanks for your order! Here are the details:</p>
        <table style="border-collapse: collapse; width: 100%; max-width: 480px;">
          <tr><td style="padding: 6px 0;"><strong>Order ID</strong></td><td>{order_id}</td></tr>
          <tr><td style="padding: 6px 0;"><strong>Product</strong></td><td>{product}</td></tr>
          <tr><td style="padding: 6px 0;"><strong>Quantity</strong></td><td>{quantity}</td></tr>
          <tr><td style="padding: 6px 0;"><strong>Delivery Address</strong></td><td>{order.get("deliveryAddress", "")}</td></tr>
        </table>
        <p>We'll be in touch with shipping updates soon.</p>
        <p style="color: #5a6470; font-size: 0.85em;">
          Azure Serverless Laptop Store — Event-Driven Order Processing System
        </p>
      </body>
    </html>
    """

    message = {
        "senderAddress": sender_address,
        "recipients": {
            "to": [{"address": recipient_email}]
        },
        "content": {
            "subject": f"Order Confirmation — {order_id}",
            "html": html_content
        }
    }

    try:
        email_client = EmailClient.from_connection_string(connection_string)
        poller = email_client.begin_send(message)
        result = poller.result()
        logging.info(
            f"Confirmation email sent for order {order_id} to {recipient_email}. "
            f"Message ID: {result.get('id', 'unknown')}"
        )
    except Exception as e:
        logging.error(f"Failed to send confirmation email for order {order_id}: {e}")


# =============================================================================
# send_rejection_email — Queue Trigger
# =============================================================================

@app.queue_trigger(
    arg_name="msg",
    queue_name="orders-invalid",
    connection="AzureWebJobsStorage"
)
def send_rejection_email(msg: func.QueueMessage) -> None:
    logging.info("send_rejection_email function triggered.")

    try:
        order = json.loads(msg.get_body().decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        logging.error(f"Failed to parse queue message as JSON: {e}")
        return

    order_id = order.get("orderId", "UNKNOWN")
    recipient_email = order.get("email")

    if not recipient_email:
        logging.error(
            f"Order {order_id} has no email address — cannot send rejection notice."
        )
        return

    connection_string = os.environ.get("ACS_CONNECTION_STRING")
    if not connection_string:
        logging.error("ACS_CONNECTION_STRING is not configured.")
        return

    sender_address = "DoNotReply@7aeee3c2-241a-4930-ac4c-9968c4d91b42.azurecomm.net"

    customer_name = order.get("customerName", "Customer")
    validation_errors = order.get("validationErrors", ["Your order could not be processed."])
    reasons_html = "".join(f"<li>{reason}</li>" for reason in validation_errors)

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #1f2933;">
        <h2 style="color: #a82020;">Order Could Not Be Processed</h2>
        <p>Hi {customer_name},</p>
        <p>
          Unfortunately we were unable to process your order
          (ID: {order_id}). Here's why:
        </p>
        <ul>{reasons_html}</ul>
        <p>
          Please review the details and submit your order again. If you
          believe this is an error, feel free to reach out.
        </p>
        <p style="color: #5a6470; font-size: 0.85em;">
          Azure Serverless Laptop Store — Event-Driven Order Processing System
        </p>
      </body>
    </html>
    """

    message = {
        "senderAddress": sender_address,
        "recipients": {
            "to": [{"address": recipient_email}]
        },
        "content": {
            "subject": f"Order Update — {order_id}",
            "html": html_content
        }
    }

    try:
        email_client = EmailClient.from_connection_string(connection_string)
        poller = email_client.begin_send(message)
        result = poller.result()
        logging.info(
            f"Rejection email sent for order {order_id} to {recipient_email}. "
            f"Message ID: {result.get('id', 'unknown')}"
        )
    except Exception as e:
        logging.error(f"Failed to send rejection email for order {order_id}: {e}")
