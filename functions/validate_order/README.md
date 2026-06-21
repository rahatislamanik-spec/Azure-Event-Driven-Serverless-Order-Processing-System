# validate_order

Queue-triggered Azure Function that validates incoming orders and routes them
based on the result.

> Implementation note: this function is implemented in
> `functions/submit_order/function_app.py` as part of the combined Python V2
> deployment package. All four functions deploy together from that file because
> Azure Functions publishes the current package as the complete Function App.

## Trigger

Queue Trigger on **`orders-incoming`**. Fires automatically whenever
`submit_order` (or any other producer) places a message on this queue — no
HTTP endpoint, no manual invocation required.

## What it does

1. Parses the incoming queue message as JSON. If parsing fails, the raw
   message body is routed to `orders-invalid` for manual review rather than
   crashing the function.
2. Re-validates the order independently of `submit_order`'s checks:
   - All required fields present (`orderId`, `customerName`, `firstName`,
     `lastName`, `email`, `phone`, `deliveryAddress`, `product`, `laptop`,
     `quantity`)
   - Email format is valid
   - Quantity is a positive whole number
3. **If validation fails** — the order (plus a `validationErrors` list
   explaining why) is sent to the `orders-invalid` dead-letter queue.
4. **If validation passes** — the order is faned out to two queues
   simultaneously:
   - `orders-to-email` (consumed by `send_confirmation_email`)
   - `orders-to-log` (consumed by `log_to_table`)

   Each queue send is attempted independently — if one fails (e.g. a
   transient Azure Storage error), the failure is logged without blocking
   the other, and the specific queue that failed is recorded in the logs.

## Why validation happens twice

`submit_order` performs basic field-presence validation before accepting an
order from the customer (fast feedback, good UX). `validate_order` performs
the same checks again independently, because:

- It is the architecturally correct validation boundary per the approved
  design (the queue is the contract between the frontend-facing layer and
  the backend processing layer)
- It protects against a message being placed on `orders-incoming` by any
  future producer that bypasses `submit_order` entirely
- It demonstrates defense-in-depth rather than relying on a single
  validation point

## Local development

```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
pip install -r requirements.txt
cp local.settings.example.json local.settings.json
# Edit local.settings.json with your real Azure Storage connection string
func start
```

Queue Trigger functions don't expose an HTTP endpoint to test directly with
curl. To test locally, manually enqueue a test message into the
`orders-incoming` queue (e.g. via Azure CLI or Azure Storage Explorer) and
watch the function host logs.

## Files

| File | Purpose |
|---|---|
| `../submit_order/function_app.py` | Combined deployment package containing `submit_order`, `validate_order`, `log_to_table`, and `send_confirmation_email` |
| `../submit_order/host.json` | Azure Functions host configuration, including queue `messageEncoding` settings |
| `../submit_order/requirements.txt` | Python dependencies for all deployed functions |
| `../submit_order/local.settings.example.json` | Template for local settings; never commit the real `local.settings.json` |
