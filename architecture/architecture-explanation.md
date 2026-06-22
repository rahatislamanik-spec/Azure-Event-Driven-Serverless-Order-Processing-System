> 📊 **Visual diagrams available:** See [architecture-diagrams-final.html](architecture-diagrams-final.html) for the full rendered architecture and order flow diagrams.

# Architecture Explanation

## Architecture Pattern

This project uses an event-driven serverless architecture. The system separates the customer-facing request from background processing by using Azure Storage Queues between Azure Functions.

## Components

- Azure Static Web Apps hosts the frontend.
- Azure Functions run the backend workflow.
- Azure Storage Queues decouple each processing stage.
- Azure Table Storage stores order records.
- Azure Communication Services sends customer emails.
- Application Insights provides observability.

## Why This Architecture Is Feasible

The project avoids unnecessary complexity such as AKS, Kubernetes, Service Bus Premium, API Management, and Cosmos DB. It uses manageable Azure services that scale appropriately for this workload while still demonstrating real cloud architecture concepts.
