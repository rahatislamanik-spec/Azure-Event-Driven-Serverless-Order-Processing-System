#!/bin/bash
# =============================================================================
# 01-resource-group-and-networking.sh
# Azure Event-Driven Serverless Order Processing System
#
# Creates the foundational Resource Group and Virtual Network for the project.
# Run this FIRST — every other script assumes this Resource Group exists.
#
# Prerequisites:
#   - Azure CLI installed (az --version)
#   - Logged in: az login
#   - Correct subscription selected (this project uses "Azure for Students")
# =============================================================================

set -e  # Exit immediately if any command fails

RESOURCE_GROUP="rg-order-processing-dev"
LOCATION="eastus"
VNET_NAME="vnet-order-processing-dev"
VNET_ADDRESS_PREFIX="10.0.0.0/16"
SUBNET_NAME="default"
SUBNET_PREFIX="10.0.0.0/24"

echo "=== Step 1: Create Resource Group ==="
# NOTE: The original architecture documented "Canada Central" as the region.
# Azure for Students subscriptions block resource creation in Canada Central
# and Canada East (confirmed via testing — RequestDisallowedByAzure policy
# error). East US was approved as the permanent region by the course
# instructor. If you hit the same policy block, try eastus, eastus2, or
# centralus as alternatives.
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$LOCATION"

echo "=== Step 2: Register required resource providers ==="
# Fresh subscriptions often need these registered manually before first use.
# This can take 1-3 minutes to propagate — the loop below waits for it.
az provider register --namespace Microsoft.Network

echo "Waiting for Microsoft.Network provider registration..."
while true; do
  state=$(az provider show --namespace Microsoft.Network --query registrationState -o tsv)
  echo "Status: $state"
  if [ "$state" = "Registered" ]; then
    break
  fi
  sleep 15
done

echo "=== Step 3: Create Virtual Network ==="
az network vnet create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$VNET_NAME" \
  --location "$LOCATION" \
  --address-prefix "$VNET_ADDRESS_PREFIX" \
  --subnet-name "$SUBNET_NAME" \
  --subnet-prefix "$SUBNET_PREFIX"

echo "=== Done ==="
echo "Resource Group: $RESOURCE_GROUP"
echo "Virtual Network: $VNET_NAME"
echo "Next: run 02-storage-account-and-queues.sh"
