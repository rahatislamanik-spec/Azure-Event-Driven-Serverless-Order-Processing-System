# Azure Event-Driven Serverless Order Processing System

## Overview

This project is a collaborative George Brown College Work Integrated Learning (WIL) project that demonstrates the design and implementation of a cloud-native, event-driven order processing platform using Microsoft Azure.

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
│   ├── professor-approval-summary.md
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
https://github.com/rahatislamanik-spec/azure-event-driven-serverless-order-processing-system

Repository Owner:
Md Rahat Islam Anik
