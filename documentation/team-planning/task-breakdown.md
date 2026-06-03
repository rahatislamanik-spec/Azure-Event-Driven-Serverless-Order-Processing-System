# Team Task Breakdown

## Project
Azure Event-Driven Serverless Order Processing System

## Team Work Split

### Rahat — Project Lead / Architecture / GitHub
- Maintain GitHub repository
- Keep README and documentation updated
- Own architecture, project evidence, and final presentation
- Review pull requests before merging
- Coordinate weekly progress

### Frontend Lead
- Build the laptop store frontend
- Create product cards
- Build the customer order form
- Add client-side validation
- Connect the form to the submit_order API endpoint

### Azure Functions Lead
- Build submit_order HTTP trigger
- Build validate_order queue trigger
- Implement basic input validation
- Implement business validation
- Implement queue fan-out workflow

### Monitoring / Data Lead
- Configure Azure Communication Services Email
- Build send_confirmation_email function
- Build log_to_table function
- Configure Application Insights
- Capture Azure evidence screenshots

## Git Workflow

Each team member should work from their own branch:

- rahat-dev
- frontend-dev
- functions-dev
- monitoring-dev

Final changes should merge into main through pull requests.
