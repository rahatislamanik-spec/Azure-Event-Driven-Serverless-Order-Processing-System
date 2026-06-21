#!/bin/bash
# =============================================================================
# 04-key-vault-and-identity.sh
# Azure Event-Driven Serverless Order Processing System
#
# Creates Key Vault, stores the Storage and ACS connection strings as
# secrets, enables Managed Identity on the Function App, and grants that
# identity read-only access to the secrets it needs. This implements the
# "Security by Design" principle from the architecture — no secrets live in
# plain text in App Settings.
#
# IMPORTANT LESSON LEARNED: This Key Vault uses RBAC authorization mode
# (the modern model). Even as the account that CREATED the vault, you will
# get a "(Forbidden) ... ForbiddenByRbac" error trying to write secrets
# until you explicitly grant yourself the "Key Vault Secrets Officer" role.
# This trips people up because vault *creation* succeeds but secret
# *management* still requires a separate, explicit role assignment.
#
# Prerequisites:
#   - 02-storage-account-and-queues.sh and 03-function-app.sh have been run
#   - 05-communication-services-email.sh has been run (for the ACS secret)
#     — if you haven't set up ACS yet, comment out the AcsConnectionString
#     section below and re-run it after.
# =============================================================================

set -e

RESOURCE_GROUP="rg-order-processing-dev"
LOCATION="eastus"
KEY_VAULT="kv-orderproc-rahat"  # Must be globally unique
STORAGE_ACCOUNT="storderstoragedev"
FUNCTION_APP="func-order-processing-dev"
ACS_NAME="acs-order-email-dev"

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

echo "=== Step 1: Create Key Vault ==="
# Note: the original intended name "kv-order-processing-dev" was globally
# taken (Key Vault names must be unique across ALL of Azure, not just your
# subscription) — hence the "-rahat" suffix fallback used here.
az keyvault create \
  --name "$KEY_VAULT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION"

echo "=== Step 2: Grant yourself Key Vault Secrets Officer role ==="
# Required even though you created the vault — RBAC mode does not
# automatically grant the creator secret-management rights.
MY_ACCOUNT=$(az account show --query user.name -o tsv)
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee "$MY_ACCOUNT" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT"

echo "Waiting 30s for role assignment to propagate..."
sleep 30

echo "=== Step 3: Store Storage connection string as a secret ==="
STORAGE_CONN=$(az storage account show-connection-string \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --query connectionString -o tsv)

az keyvault secret set \
  --vault-name "$KEY_VAULT" \
  --name "StorageConnectionString" \
  --value "$STORAGE_CONN" \
  --output none

echo "=== Step 4: Store ACS connection string as a secret ==="
ACS_CONN=$(az communication list-key \
  --name "$ACS_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query primaryConnectionString -o tsv)

az keyvault secret set \
  --vault-name "$KEY_VAULT" \
  --name "AcsConnectionString" \
  --value "$ACS_CONN" \
  --output none

echo "=== Step 5: Enable Managed Identity on the Function App ==="
IDENTITY_PRINCIPAL_ID=$(az functionapp identity assign \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --query principalId -o tsv)

echo "Function App Managed Identity principalId: $IDENTITY_PRINCIPAL_ID"

echo "=== Step 6: Grant the Function App's identity read access to Key Vault ==="
# "Key Vault Secrets User" is a READ-ONLY role — least privilege. The
# Function App can fetch secret values at runtime but cannot create, edit,
# or delete them.
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee "$IDENTITY_PRINCIPAL_ID" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT"

echo "=== Step 7: Point Function App settings at Key Vault instead of plain text ==="
az functionapp config appsettings set \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --settings "AzureWebJobsStorage=@Microsoft.KeyVault(SecretUri=https://$KEY_VAULT.vault.azure.net/secrets/StorageConnectionString/)" \
  --output none

az functionapp config appsettings set \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --settings "ACS_CONNECTION_STRING=@Microsoft.KeyVault(SecretUri=https://$KEY_VAULT.vault.azure.net/secrets/AcsConnectionString/)" \
  --output none

echo "=== Done ==="
echo "Key Vault: $KEY_VAULT"
echo "Secrets stored: StorageConnectionString, AcsConnectionString"
echo "Function App now authenticates via Managed Identity — no plain-text"
echo "secrets remain in App Settings."
