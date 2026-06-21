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


## Security Model — Key Vault and Managed Identity

Secrets (the storage account connection string and the Azure Communication
Services connection string) are not stored as plain text anywhere in the
Function App configuration. Instead:

1. Both values are stored as secrets in Azure Key Vault (`kv-orderproc-rahat`):
   - `StorageConnectionString`
   - `AcsConnectionString`
2. The Function App (`func-order-processing-dev`) has a System-Assigned
   Managed Identity enabled, giving it its own Azure AD identity.
3. That identity is granted the **Key Vault Secrets User** role (read-only)
   on the vault — least privilege, since the Function App only needs to read
   secrets at runtime, never create or modify them.
4. The Function App's `AzureWebJobsStorage` and `ACS_CONNECTION_STRING`
   settings use Key Vault reference syntax instead of plain values:

   ```
   AzureWebJobsStorage = @Microsoft.KeyVault(SecretUri=https://kv-orderproc-rahat.vault.azure.net/secrets/StorageConnectionString/)
   ACS_CONNECTION_STRING = @Microsoft.KeyVault(SecretUri=https://kv-orderproc-rahat.vault.azure.net/secrets/AcsConnectionString/)
   ```

The vault uses RBAC authorization mode rather than legacy access policies.
Anyone managing secrets directly (not just reading them at runtime) needs
the **Key Vault Secrets Officer** role assigned explicitly — this isn't
granted automatically just by being the vault's creator.
