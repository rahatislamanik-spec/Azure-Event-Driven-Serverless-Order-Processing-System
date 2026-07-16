> 📊 **Visual diagrams available:** See [architecture-diagrams-final.html](architecture-diagrams-final.html) for the full rendered architecture and order flow diagrams.

# High-Level Project Flow

```text
Customer
  ↓
Azure Static Web App
  ↓
submit_order Function
  ↓
orders-incoming Queue
  ↓
validate_order Function
  ├── Invalid order → orders-invalid Queue
  └── Valid order → Fan-out
          ├── orders-to-email Queue → send_confirmation_email Function → ACS Email
          └── orders-to-log Queue → log_to_table Function → Azure Table Storage

All functions → Application Insights / Azure Monitor
```
