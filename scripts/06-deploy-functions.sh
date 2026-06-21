#!/bin/bash
# =============================================================================
# 06-deploy-functions.sh
# Azure Event-Driven Serverless Order Processing System
#
# Sets up the local Python environment and deploys all four functions
# (submit_order, validate_order, log_to_table, send_confirmation_email) to
# the live Function App.
#
# IMPORTANT LESSONS LEARNED (the hard way):
#
# 1. ALL FOUR FUNCTIONS MUST LIVE IN ONE function_app.py FILE.
#    `func azure functionapp publish` deploys the ENTIRE current directory
#    as the complete package for the Function App. If each function lives in
#    its own separate folder and you deploy from each folder independently,
#    EACH DEPLOY COMPLETELY REPLACES whatever was deployed before it — we
#    lost submit_order entirely the first time validate_order was deployed
#    this way. The Python V2 programming model supports multiple functions
#    in a single file using multiple @app.route / @app.queue_trigger
#    decorators — that is the correct approach for a multi-function app
#    deployed as one unit.
#
# 2. LOCAL PYTHON VERSION MUST MATCH THE DEPLOYED RUNTIME (3.11).
#    macOS system Python is often an old 3.9.x. Using it locally causes
#    "ModuleNotFound" risk and deployment warnings. Always use a dedicated
#    virtual environment built from Python 3.11 specifically.
#
# 3. requirements.txt MUST LIST EVERY DEPENDENCY EXPLICITLY.
#    A missing dependency does NOT throw a clear error. The remote build
#    reports "succeeded," but the Python worker silently fails to import the
#    module and ZERO functions register — `az functionapp function list`
#    returns an empty array with no explanation anywhere in the logs.
#
# 4. QUEUE TRIGGER MESSAGES NEED messageEncoding: "none" IN host.json.
#    Azure Functions' queue trigger binding defaults to expecting
#    Base64-encoded message content. If your code sends plain JSON text via
#    the Storage Queue SDK directly (queue_client.send_message(json.dumps(..))),
#    every message will silently fail to decode at the BINDING level —
#    before your Python code ever runs. No traceback, no error, nothing —
#    just messages quietly moving to the poison queue after 5 retries. This
#    cost the most debugging time of the entire project. The fix is one
#    block in host.json (see the host.json template included in this repo):
#      "extensions": { "queues": { "messageEncoding": "none" } }
#
# 5. submit_order NEEDS auth_level=func.AuthLevel.ANONYMOUS EXPLICITLY.
#    The Python V2 model defaults to FUNCTION-level auth (requires a
#    function key). A public customer-facing order endpoint should not
#    require a key — set this explicitly in the @app.route decorator.
#
# Prerequisites:
#   - 03-function-app.sh has been run (the Function App must already exist)
#   - Homebrew installed (for installing Python 3.11 on macOS)
#   - The combined function_app.py, host.json, and requirements.txt from
#     this repo's functions/submit_order/ folder
# =============================================================================

set -e

RESOURCE_GROUP="rg-order-processing-dev"
FUNCTION_APP="func-order-processing-dev"
PROJECT_DIR="functions/submit_order"  # Where the combined function_app.py lives

echo "=== Step 1: Install Python 3.11 if not already present ==="
if [ ! -f "/opt/homebrew/bin/python3.11" ]; then
  brew install python@3.11
fi

echo "=== Step 2: Create and activate a dedicated virtual environment ==="
cd "$PROJECT_DIR"
/opt/homebrew/bin/python3.11 -m venv .venv311
source .venv311/bin/activate
python --version  # Should print Python 3.11.x

echo "=== Step 3: Install dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Step 4: Configure local.settings.json (local testing only) ==="
if [ ! -f "local.settings.json" ]; then
  cp local.settings.example.json local.settings.json
  STORAGE_CONN=$(az storage account show-connection-string \
    --name storderstoragedev \
    --resource-group "$RESOURCE_GROUP" \
    --query connectionString -o tsv)
  python -c "
import json
with open('local.settings.json') as f:
    data = json.load(f)
data['Values']['AzureWebJobsStorage'] = '''$STORAGE_CONN'''
with open('local.settings.json', 'w') as f:
    json.dump(data, f, indent=2)
print('local.settings.json configured')
"
fi

echo "=== Step 5: (Optional) Test locally before deploying ==="
echo "Run 'func start' in another terminal to test locally first."
echo "Press Enter to continue with deployment, or Ctrl+C to test locally first."
read -r

echo "=== Step 6: Deploy to Azure ==="
func azure functionapp publish "$FUNCTION_APP" --python

echo "=== Step 7: Verify all four functions registered ==="
az functionapp function list \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --query "[].name" -o tsv

echo "=== Done ==="
echo "Expected output above: submit_order, validate_order, log_to_table,"
echo "send_confirmation_email — all four. If any are missing, check"
echo "requirements.txt for missing dependencies (see Lesson 3 above)."
