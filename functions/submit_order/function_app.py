import azure.functions as func
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from azure.storage.queue import QueueClient

app = func.FunctionApp()


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
    missing_fields = [field for field in required_fields if not order.get(field)]

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
