#!/bin/bash
# =============================================================================
# 03-function-app.sh
# Azure Event-Driven Serverless Order Processing System
#
# Creates the Function App that hosts all four backend functions
# (submit_order, validate_order, log_to_table, send_confirmation_email).
#
# IMPORTANT LESSON LEARNED: Creating this via the Azure Portal GUI is risky —
# selecting "Consumption (Windows)" as the hosting plan silently locks the
# Operating System to Windows, which hides Python entirely from the runtime
# stack dropdown (Python only runs on Linux Function Apps). The CLI command
# below avoids this trap entirely by specifying --os-type Linux directly.
#
# Prerequisites:
#   - 02-storage-account-and-queues.sh has been run successfully
#     (the Function App needs an existing Storage Account to link to)
# =============================================================================

set -e

RESOURCE_GROUP="rg-order-processing-dev"
LOCATION="eastus"
STORAGE_ACCOUNT="storderstoragedev"
FUNCTION_APP="func-order-processing-dev"  # Must be globally unique

echo "=== Step 1: Register Microsoft.Web provider ==="
az provider register --namespace Microsoft.Web

echo "Waiting for Microsoft.Web provider registration..."
while true; do
  state=$(az provider show --namespace Microsoft.Web --query registrationState -o tsv)
  echo "Status: $state"
  if [ "$state" = "Registered" ]; then
    break
  fi
  sleep 15
done

echo "=== Step 2: Create Function App ==="
# --os-type Linux is mandatory for Python. --runtime-version 3.11 must match
# the local Python virtual environment used for development (see
# 06-deploy-functions.sh) or the remote build will warn about a version
# mismatch and may fail to register functions correctly.
az functionapp create \
  --resource-group "$RESOURCE_GROUP" \
  --consumption-plan-location "$LOCATION" \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name "$FUNCTION_APP" \
  --storage-account "$STORAGE_ACCOUNT" \
  --os-type Linux

echo "=== Step 3: Configure CORS for the frontend ==="
# Allows the browser-hosted frontend (frontend/index.html) to call
# submit_order without being blocked by the browser's same-origin policy.
# "*" (allow all origins) is acceptable for this dev/student project;
# a production system should restrict this to the actual frontend's domain.
az functionapp cors add \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --allowed-origins "*"

echo "=== Done ==="
echo "Function App: $FUNCTION_APP"
echo "Note: Application Insights and a default Log Analytics Workspace are"
echo "auto-created by Azure alongside this Function App."
echo "Next: run 04-key-vault-and-identity.sh"
