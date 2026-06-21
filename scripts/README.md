# Infrastructure Build Scripts

These scripts rebuild the entire Azure infrastructure for the
**Azure Event-Driven Serverless Order Processing System** from scratch,
in the order they were actually used to build this project. They are not
idealized or theoretical — each one reflects real commands run against a
live Azure for Students subscription, including the fixes for real problems
encountered along the way.

## Why these exist

Anyone reviewing this repository — a professor, a teammate, or a future
employer — can read these scripts top to bottom and understand exactly:

- What Azure resources this project depends on
- The order in which they must be created (and why)
- The real, non-obvious problems that came up during a from-scratch build,
  and how each was diagnosed and fixed

This is intentionally not a polished "happy path only" set of commands.
The comments inside each script document genuine lessons learned — several
of which took significant debugging time to discover (see
`06-deploy-functions.sh` in particular for the queue message encoding
issue, which was the hardest bug in the entire project).

## Run order

```
01-resource-group-and-networking.sh
02-storage-account-and-queues.sh
03-function-app.sh
05-communication-services-email.sh   (can run any time after 01)
04-key-vault-and-identity.sh         (run AFTER 02, 03, and 05 —
                                       it stores secrets from both)
06-deploy-functions.sh
```

Note the Key Vault script is numbered `04` but should be run *after*
`05` (Communication Services), since it stores the ACS connection string
as one of its secrets. The numbering reflects architectural grouping
(Key Vault is conceptually a "core" resource), not strict execution order —
this run order list above is the actual sequence to follow.

## Prerequisites

- Azure CLI installed and you are logged in (`az login`)
- An active Azure subscription with permission to create resources
  (this project was built on Azure for Students)
- Homebrew (macOS) for installing Python 3.11, used in
  `06-deploy-functions.sh`
- This repository cloned locally, with `functions/submit_order/` containing
  the combined `function_app.py`, `host.json`, and `requirements.txt`

## Region note

These scripts default to **East US**. The original architecture
documentation specified Canada Central, but Azure for Students subscriptions
block resource creation in Canada Central and Canada East (confirmed via
direct testing — `RequestDisallowedByAzure` policy error). East US was
approved as the permanent region by the course instructor after this was
discovered. If you're running these scripts on a different subscription
without this restriction, you can change the `LOCATION` variable in each
script.

## Naming collisions

Two resource names had to change from the originally planned names because
they were already taken globally (Storage Account and Key Vault names must
be unique across ALL of Azure, not just your subscription):

- Key Vault: `kv-order-processing-dev` → `kv-orderproc-rahat`

If you hit a similar naming collision running these scripts under your own
account, just change the relevant variable at the top of the script — Azure
will tell you immediately if a name is taken.

## What these scripts do NOT do

- They do not deploy the actual function code logic changes — that's a
  one-time setup in `06-deploy-functions.sh`, but ongoing code changes
  should just re-run `func azure functionapp publish` directly, not the
  whole script
- They do not set up Application Insights alerting rules or Log Analytics
  queries (Phase 7 — Monitoring & Observability, documented separately)
- They do not include the frontend deployment (Azure Static Web Apps) —
  see `frontend/` and the project roadmap for that
