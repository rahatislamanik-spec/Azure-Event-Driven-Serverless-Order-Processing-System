# send_confirmation_email

Queue-triggered Azure Function that sends customer order confirmation emails
through Azure Communication Services.

> Implementation note: this function is implemented in
> `functions/submit_order/function_app.py` as part of the combined Python V2
> deployment package. All four functions deploy together from that file because
> Azure Functions publishes the current package as the complete Function App.

## Trigger

Queue Trigger on **`orders-to-email`**. The function runs automatically after
`validate_order` confirms an order is valid and places an email work item on
the queue.

## What it does

1. Reads the validated order message from `orders-to-email`.
2. Parses the order details.
3. Builds an HTML confirmation email containing the order ID, product,
   quantity, and delivery information.
4. Sends the message through Azure Communication Services Email.
5. Logs delivery submission status through the Function App runtime logs.

## Why this function exists

Email delivery is handled as a separate queue-triggered function so customer
notification can scale independently from validation and database logging. If
email delivery is delayed or temporarily unavailable, the logging path can still
continue without blocking the full order pipeline.

## Architecture role

| Item | Value |
| --- | --- |
| Trigger type | Azure Storage Queue trigger |
| Source queue | `orders-to-email` |
| Email provider | Azure Communication Services Email |
| Runtime | Python Azure Functions v2 |
| Deployment package | `functions/submit_order/function_app.py` |

## Azure Communication Services resources

The live test used:

* `acs-order-email-dev` — Azure Communication Services resource
* `acs-order-email-service-dev` — Email Communication Service resource
* Azure Managed Domain — auto-verified sender domain

## Local testing notes

Queue-triggered functions do not expose HTTP endpoints. To test this function,
run the combined Function App locally, place a valid order message on
`orders-to-email`, and verify that the email submission appears in the function
logs and in the recipient inbox.
