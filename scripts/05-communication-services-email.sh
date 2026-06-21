#!/bin/bash
# =============================================================================
# 05-communication-services-email.sh
# Azure Event-Driven Serverless Order Processing System
#
# Creates Azure Communication Services, an Email Communication Service, and
# links a free Azure Managed Domain for sending confirmation emails.
#
# IMPORTANT LESSON LEARNED: A custom domain requires DNS verification that
# can take 1-3 days for Microsoft to approve. The Azure Managed Domain used
# here is INSTANTLY verified — DKIM, DKIM2, DMARC, Domain, and SPF all show
# "Verified" status immediately upon creation, with zero DNS configuration
# required. This is the right choice for a dev/student project on a deadline;
# a production system serving real customers would typically use a verified
# custom domain instead, for branding and deliverability reasons.
#
# Prerequisites:
#   - 01-resource-group-and-networking.sh has been run
# =============================================================================

set -e

RESOURCE_GROUP="rg-order-processing-dev"
ACS_NAME="acs-order-email-dev"
EMAIL_SERVICE_NAME="acs-order-email-service-dev"

echo "=== Step 1: Register Microsoft.Communication provider ==="
az provider register --namespace Microsoft.Communication

echo "Waiting for Microsoft.Communication provider registration..."
while true; do
  state=$(az provider show --namespace Microsoft.Communication --query registrationState -o tsv)
  echo "Status: $state"
  if [ "$state" = "Registered" ]; then
    break
  fi
  sleep 15
done

echo "=== Step 2: Create Communication Services resource ==="
az communication create \
  --name "$ACS_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location global \
  --data-location unitedstates

echo "=== Step 3: Create Email Communication Service ==="
az communication email create \
  --name "$EMAIL_SERVICE_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location global \
  --data-location unitedstates

echo "=== Step 4: Create and auto-verify the Azure Managed Domain ==="
az communication email domain create \
  --domain-name "AzureManagedDomain" \
  --email-service-name "$EMAIL_SERVICE_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location global \
  --domain-management AzureManaged

echo "=== Step 5: Link the domain to the Communication Services resource ==="
DOMAIN_ID="/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Communication/emailServices/$EMAIL_SERVICE_NAME/domains/AzureManagedDomain"

az communication update \
  --name "$ACS_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --linked-domains "$DOMAIN_ID"

echo "=== Done ==="
echo "Communication Services: $ACS_NAME"
echo "Email Service: $EMAIL_SERVICE_NAME"
echo "Domain: AzureManagedDomain (auto-verified)"
echo ""
echo "Sender address will be in the format:"
echo "  DoNotReply@<unique-id>.azurecomm.net"
echo ""
echo "Run this to find your exact sender domain (needed in function_app.py):"
echo "  az communication email domain show --domain-name AzureManagedDomain \\"
echo "    --email-service-name $EMAIL_SERVICE_NAME --resource-group $RESOURCE_GROUP \\"
echo "    --query mailFromSenderDomain -o tsv"
echo ""
echo "Next: run 04-key-vault-and-identity.sh (if not already done) to store"
echo "the ACS connection string securely."
