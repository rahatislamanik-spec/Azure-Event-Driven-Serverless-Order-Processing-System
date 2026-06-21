# log_to_table

Queue-triggered Azure Function that writes validated orders to Azure Table Storage.

> Implementation note: this function is implemented in
> `functions/submit_order/function_app.py` as part of the combined Python V2
> deployment package. All four functions deploy together from that file because
> Azure Functions publishes the current package as the complete Function App.

## Trigger

Queue Trigger on **`orders-to-log`**. The function runs automatically after
`validate_order` confirms an order is valid and places a logging work item on
the queue.

## What it does

1. Reads the validated order message from `orders-to-log`.
2. Parses the message as JSON.
3. Builds a table entity using the order ID and customer/order details.
4. Writes the entity to the `Orders` Azure Table Storage table.
5. Logs success or failure through the Function App runtime logs.

## Why this function exists

The order logging step is separated from validation and email delivery so that
database persistence can succeed or fail independently. This keeps the backend
event-driven and avoids coupling customer notification to storage writes.

## Architecture role

| Item | Value |
| --- | --- |
| Trigger type | Azure Storage Queue trigger |
| Source queue | `orders-to-log` |
| Destination | Azure Table Storage `Orders` table |
| Runtime | Python Azure Functions v2 |
| Deployment package | `functions/submit_order/function_app.py` |

## Local testing notes

Queue-triggered functions do not expose HTTP endpoints. To test this function,
run the combined Function App locally, place a valid order message on
`orders-to-log`, and verify that a row appears in the `Orders` table.
