# submit_order Function

This folder contains the combined Python V2 Azure Functions deployment package for the order processing workflow. The original entry point is `submit_order`, and the same `function_app.py` file now also contains `validate_order`, `log_to_table`, and `send_confirmation_email`.

## Purpose

`submit_order` is the HTTP entry point for the application. It receives a laptop order from the frontend form, validates the request, creates an order ID, normalizes the payload, and sends the order message to the `orders-incoming` Azure Storage Queue.

## Trigger and Route

| Setting | Value |
| --- | --- |
| Programming model | Python Azure Functions v2 |
| Trigger type | HTTP trigger |
| Route | `/api/submit_order` |
| Method | `POST` |
| Authorization level | `ANONYMOUS` |
| Queue output | `orders-incoming` |
| Deployment model | Combined Function App package |

## Request Fields

The function expects JSON with these fields:

| Field | Purpose |
| --- | --- |
| `firstName` | Customer first name |
| `lastName` | Customer last name |
| `email` | Customer email address |
| `phone` | Customer phone number |
| `deliveryAddress` | Delivery address from the frontend form |
| `laptop` | Selected laptop model |
| `quantity` | Quantity ordered |

## Validation

The function validates:

* Required fields are present
* Email contains a basic valid format
* Quantity is a positive whole number
* `AzureWebJobsStorage` is configured before writing to the queue

On success, the function returns HTTP `202 Accepted` with an `orderId`.

## Local Run

From this folder:

```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
pip install -r requirements.txt
cp local.settings.example.json local.settings.json
func start
```

Before running locally, update `local.settings.json` with a valid `AzureWebJobsStorage` value or use a local storage emulator if available.

## Example Test

```bash
curl -X POST http://localhost:7071/api/submit_order \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "phone": "5551234567",
    "deliveryAddress": "123 Example Street",
    "laptop": "AzureBook Air 13",
    "quantity": 1
  }'
```

## Combined Deployment Package

Azure Functions publishes the current deployment directory as the complete Function App package. For this project, all four functions live together in `function_app.py` so a deployment does not accidentally replace previously deployed functions.

The combined package includes:

* `submit_order` — HTTP trigger that accepts the order and writes to `orders-incoming`
* `validate_order` — Queue trigger that validates and fans out orders
* `log_to_table` — Queue trigger that writes validated orders to Azure Table Storage
* `send_confirmation_email` — Queue trigger that sends confirmation email through Azure Communication Services

## Deployment Notes

The combined package has been deployed to the Azure Function App `func-order-processing-dev`. During deployment, the Python 3.11 runtime and the required Azure SDK dependencies were needed for the functions to register and process queue, table, and email operations.

`host.json` also includes queue `messageEncoding` configuration so Storage Queue trigger messages written as plain JSON can be processed correctly by the Function App runtime.
