# Azure Event-Driven Serverless Order Processing System

A production-oriented Microsoft Azure project demonstrating event-driven architecture, serverless computing, asynchronous queue-based processing, fan-out design, automated email confirmation, database logging, and centralized observability.

## Project Status

Build starting / proposal approved stage. This repository is being developed as a George Brown College Work Integrated Project.

## Project Objective

The goal of this project is to build a serverless order processing system where a customer submits a laptop order from a web app and receives a fast response while backend processing happens asynchronously.

The system uses Azure Static Web Apps, Azure Functions, Azure Storage Queues, Azure Table Storage, Azure Communication Services Email, and Azure Monitor with Application Insights.

## High-Level Flow

1. Customer submits an order through the frontend web app.
2. `submit_order` HTTP-trigger Azure Function validates the basic input.
3. Valid orders are placed into the `orders-incoming` Azure Storage Queue.
4. `validate_order` queue-trigger Azure Function performs business validation.
5. Invalid orders are routed to `orders-invalid`.
6. Valid orders are fanned out into `orders-to-email` and `orders-to-log`.
7. `send_confirmation_email` sends an email using Azure Communication Services.
8. `log_to_table` saves the confirmed order into Azure Table Storage.
9. Application Insights collects logs, metrics, traces, and errors.

## Azure Services Used

| Service | Purpose |
|---|---|
| Azure Static Web Apps | Hosts the frontend order form |
| Azure Functions | Serverless backend processing |
| Azure Storage Queues | Durable asynchronous message processing |
| Azure Table Storage | NoSQL order record storage |
| Azure Communication Services Email | Customer confirmation email |
| Azure Monitor / Application Insights | Logs, traces, metrics, alerts, and observability |

## Repository Structure

```text
.
├── architecture/
├── documentation/
├── frontend/
├── functions/
│   ├── submit_order/
│   ├── validate_order/
│   ├── send_confirmation_email/
│   └── log_to_table/
├── sample-data/
├── screenshots/
├── host.json
├── local.settings.example.json
├── requirements.txt
└── README.md
```

## Important Technical Note

`orders-invalid` is implemented as a custom invalid-orders queue. Azure Storage Queues support poison-message behavior, but they do not provide the same built-in Dead-Letter Queue feature as Azure Service Bus.

## Author

Md Rahat Islam Anik  
GitHub: rahatislamanik-spec  
Portfolio: rahatislamanik-spec.github.io/IT-Portfolio-Rahat-Islam-Anik
