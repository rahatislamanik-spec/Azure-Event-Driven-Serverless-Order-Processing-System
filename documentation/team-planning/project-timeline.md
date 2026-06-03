# Project Timeline

## Phase 1 — Planning and Repository Setup
- Create GitHub repository
- Add README
- Add architecture documentation
- Add team planning files
- Invite collaborators

## Phase 2 — Frontend Build
- Build laptop store interface
- Build order form
- Add client-side validation
- Generate JSON order payload

## Phase 3 — Azure Function Entry Point
- Build submit_order HTTP trigger
- Validate incoming requests
- Generate order ID and timestamp
- Return order received response

## Phase 4 — Queue-Based Processing
- Create Azure Storage Account
- Create orders-incoming queue
- Send valid orders to queue
- Build validate_order queue trigger

## Phase 5 — Fan-Out Processing
- Create orders-to-email queue
- Create orders-to-log queue
- Create orders-invalid queue
- Route valid and invalid orders correctly

## Phase 6 — Email and Database Integration
- Configure Azure Communication Services Email
- Send order confirmation email
- Create Orders table in Azure Table Storage
- Log validated orders to table

## Phase 7 — Monitoring and Evidence
- Enable Application Insights
- Capture function execution logs
- Capture queue screenshots
- Capture table records
- Capture confirmation email screenshot
- Prepare final presentation evidence
