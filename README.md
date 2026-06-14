# Azure Event-Driven Serverless Order Processing System
> **Status:** Architecture Complete
> **Last Updated:** June 2026

## Overview

This project demonstrates the design and implementation of a cloud-native, event-driven order processing platform using Microsoft Azure — built collaboratively by a 5-person development team, with Md Rahat Islam Anik serving as repository owner.

The solution leverages serverless computing, asynchronous messaging, queue-based workflows, automated email notifications, centralized logging, and cloud observability to simulate a production-oriented order processing environment.

---

## Project Objectives

* Build a cloud-native order processing application
* Implement event-driven architecture patterns
* Utilize Azure Functions for serverless processing
* Implement asynchronous messaging using Azure Storage Queues
* Store order data in Azure Table Storage
* Send automated customer confirmation emails
* Monitor application health using Azure Monitor and Application Insights
* Demonstrate collaborative GitHub development workflows

---

## Azure Services Used

| Service                      | Purpose                   |
| ---------------------------- | ------------------------- |
| Azure Static Web Apps        | Frontend hosting          |
| Azure Functions              | Serverless compute        |
| Azure Storage Queues         | Asynchronous processing   |
| Azure Table Storage          | Order persistence         |
| Azure Communication Services | Email notifications       |
| Azure Monitor                | Monitoring and alerting   |
| Application Insights         | Logging and observability |

---

## High-Level Architecture

Customer

↓

Azure Static Web App

↓

submit_order Function

↓

orders-incoming Queue

↓

validate_order Function

↓

Fan-Out Processing

├── orders-to-email Queue

├── orders-to-log Queue

└── orders-invalid Queue

↓

Azure Communication Services Email

↓

Azure Table Storage

↓

Application Insights

---

## Repository Structure

```text
.
├── architecture/
├── documentation/
│   ├── deployment-guide.md
│   ├── stakeholder-approval-summary.md
│   ├── meeting-notes/
│   └── team-planning/
├── frontend/
├── functions/
│   ├── submit_order/
│   ├── validate_order/
│   ├── send_confirmation_email/
│   └── log_to_table/
├── sample-data/
├── evidence/
├── screenshots/
├── host.json
├── requirements.txt
└── README.md
```

---

## Development Workflow

This project follows a collaborative GitHub workflow:

```text
Issue
↓
Development Branch
↓
Commit
↓
Push
↓
Pull Request
↓
Review
↓
Merge into Main
```

Primary branches:

* main
* rahat-dev

Additional team branches will be created as development progresses.

---

## Project Team

### Team Lead

* Hikmat

### Team Members

* Md Rahat Islam Anik (Repository Owner)
* Yatish
* Devansh
* Puneet
* Ashdeep

---

## Repository Ownership

This repository is hosted and maintained under the GitHub account of Md Rahat Islam Anik (`rahatislamanik-spec`) for project coordination, source control management, pull request reviews, and collaborative development.

All architecture, code, documentation, testing, and deployment activities are performed collaboratively by the project team.

---

## Project Status

Current Status: Planning and Development Phase

Completed:

* Repository creation
* Architecture design
* Documentation structure
* Team planning
* GitHub Issues creation
* Branching strategy implementation

In Progress:

* Frontend development
* Azure infrastructure implementation

---

## GitHub Repository

Repository:
https://github.com/rahatislamanik-spec/Azure-Event-Driven-Serverless-Order-Processing-System

Repository Owner:
Md Rahat Islam Anik


## Project Team

This project was developed collaboratively, focused on Azure serverless computing, event-driven architecture, cloud-native application development, and observability.

### Project Timeline

**Project Duration:** May 2026 – August 2026

The project is currently in the Planning & Architecture phase. The team is finalizing requirements, infrastructure design, development responsibilities, and implementation strategy before moving into full-scale development.

Development is being completed in multiple phases, with the repository updated regularly to reflect architecture, implementation progress, testing evidence, and deployment artifacts.

### Project Status

**Current Phase:** Planning & Architecture

#### Progress Overview

* ✅ Project proposal approved
* ✅ Logical architecture completed
* ✅ Initial GitHub repository established
* ✅ Team collaboration workflow established
* ✅ Initial planning documentation completed
* ⏳ Infrastructure architecture design
* ⏳ Azure resource deployment
* ⏳ Frontend implementation
* ⏳ Azure Functions implementation
* ⏳ Testing and validation

### Team Lead

* Hikmatullah Shinwari — Team Lead
* Md Rahat Islam Anik — GitHub Repository Owner & Team Member

### Team Members

* Md Rahat Islam Anik — GitHub Repository Owner & Team Member
* Yatish Yashwant Vispute — Team Member
* Devansh Mehulkumar Bhatt — Team Member
* Ashdeep Singh Grewal — Team Member
* Puneet Singh — Team Member


### Team Collaboration

The project is being developed collaboratively using GitHub Issues, feature branches, pull requests, code reviews, and shared documentation. Team members are responsible for different project components and contribute incrementally throughout the project lifecycle.

All major updates, architecture changes, implementation milestones, testing evidence, and project documentation will be maintained within this repository.

### Repository Ownership

This repository is hosted under the GitHub account of Md Rahat Islam Anik (`rahatislamanik-spec`) for source control, documentation management, pull request reviews, and team collaboration purposes.

All architecture, documentation, implementation, testing, and project deliverables are developed collaboratively by the project team.





