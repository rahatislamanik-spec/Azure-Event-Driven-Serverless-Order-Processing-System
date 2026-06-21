#!/bin/bash
# =============================================================================
# 02-storage-account-and-queues.sh
# Azure Event-Driven Serverless Order Processing System
#
# Creates the Storage Account, the 4 Storage Queues, and the Orders table.
# This is the messaging and data backbone of the entire event-driven pipeline.
#
# Prerequisites:
#   - 01-resource-group-and-networking.sh has been run successfully
# =============================================================================

set -e

RESOURCE_GROUP="rg-order-processing-dev"
LOCATION="eastus"
STORAGE_ACCOUNT="storderstoragedev"  # Must be globally unique, lowercase, no hyphens, 3-24 chars

echo "=== Step 1: Register Microsoft.Storage provider ==="
az provider register --namespace Microsoft.Storage

echo "Waiting for Microsoft.Storage provider registration..."
while true; do
  state=$(az provider show --namespace Microsoft.Storage --query registrationState -o tsv)
  echo "Status: $state"
  if [ "$state" = "Registered" ]; then
    break
  fi
  sleep 15
done

echo "=== Step 2: Create Storage Account ==="
az storage account create \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --sku Standard_LRS \
  --kind StorageV2

echo "=== Step 3: Create Storage Queues ==="
az storage queue create --name orders-incoming --account-name "$STORAGE_ACCOUNT"
az storage queue create --name orders-to-email --account-name "$STORAGE_ACCOUNT"
az storage queue create --name orders-to-log --account-name "$STORAGE_ACCOUNT"
az storage queue create --name orders-invalid --account-name "$STORAGE_ACCOUNT"

echo "=== Step 4: Create Orders table ==="
az storage table create --name Orders --account-name "$STORAGE_ACCOUNT"

echo "=== Done ==="
echo "Storage Account: $STORAGE_ACCOUNT"
echo "Queues created: orders-incoming, orders-to-email, orders-to-log, orders-invalid"
echo "Table created: Orders"
echo "Next: run 03-function-app.sh"
