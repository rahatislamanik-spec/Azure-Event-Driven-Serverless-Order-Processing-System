# Deployment Guide

## GitHub First Push

```bash
git init
git add .
git commit -m "Initial project scaffold for Azure serverless order processing system"
git branch -M main
git remote add origin https://github.com/rahatislamanik-spec/Azure-Event-Driven-Serverless-Order-Processing-System.git
git push -u origin main
```

## Azure Resources To Create

1. Resource Group
2. Storage Account
3. Queues: orders-incoming, orders-to-email, orders-to-log, orders-invalid
4. Orders table
5. Function App
6. Application Insights
7. Static Web App
8. Azure Communication Services Email
