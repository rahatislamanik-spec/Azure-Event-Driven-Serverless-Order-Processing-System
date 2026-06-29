# Azure Event-Driven Serverless Order Processing System
> **Status:** Phase 8 Complete — Live on Azure  |  Last Updated: June 2026

## 🚀 Live Demo

| | Link |
|---|---|
| 🛒 **Order Form** | [Launch Storefront](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/) |
| 📁 **Evidence Gallery** | [View All 53 Screenshots](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/evidence/evidence-gallery.html) |
| 📊 **Architecture & Flow Diagrams** | [View Diagrams](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/architecture/architecture-diagrams-final.html) |
| 🗺️ **Project Roadmap** | [View Roadmap](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/roadmap/project-roadmap-build-plan.html) |
| 🏗️ **Architecture Overview** | [View Overview](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/architecture/project-architecture-overview.html) |

---

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
* Send automated customer confirmation and rejection emails
* Monitor application health using Azure Monitor and Application Insights
* Demonstrate collaborative GitHub development workflows

---

## Azure Services Used

| Service                      | Purpose                   |
| ---------------------------- | ------------------------- |
| GitHub Pages | Frontend hosting — approved substitute for Azure Static Web Apps (blocked on all supported regions under Azure for Students subscription, approved by Professor Ali Ziyaei, June 22, 2026) |
| Azure Functions              | Serverless compute        |
| Azure Storage Queues         | Asynchronous processing   |
| Azure Table Storage          | Order and inventory persistence |
| Azure Communication Services | Confirmation and rejection email notifications |
| Azure Monitor                | Monitoring and alerting   |
| Application Insights         | Logging and observability |

---

## High-Level Architecture

Customer

↓

CoreTech Store (GitHub Pages)

↓

submit_order Function

↓

orders-incoming Queue

↓

validate_order Function

↓

LaptopInventory Table

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
│   ├── submit_order/          ← combined function_app.py (all 5 functions, Python V2 model)
│   ├── validate_order/        ← README only, implementation in submit_order/function_app.py
│   ├── send_confirmation_email/ ← README only, implementation in submit_order/function_app.py
│   ├── send_rejection_email/  ← README only, implementation in submit_order/function_app.py
│   └── log_to_table/          ← README only, implementation in submit_order/function_app.py
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

Current Status: Phase 8 Complete — Live on Azure

Completed:

* Repository creation
* Architecture design
* Documentation structure
* Team planning
* GitHub Issues creation
* Branching strategy implementation
* Phase 1 Azure infrastructure provisioning
* Phase 2 frontend connection to live Function App endpoint
* Phase 3 `submit_order` Function App deployment and browser/curl validation
* Phase 4 `validate_order` queue-triggered validation and fan-out
* Phase 5 `log_to_table`, `send_confirmation_email`, and `send_rejection_email` processing functions
* Phase 6 security hardening with Key Vault-backed settings and Managed Identity
* Phase 7 monitoring and observability configuration
* Revision 4 scope expansion: `LaptopInventory` stock tracking with validation-time stock checks and decrement logic
* Phase 8 test matrix covering valid orders, missing fields, invalid email, zero quantity, insufficient stock, and unknown laptop models
* Frontend hosted via GitHub Pages — Azure Static Web Apps blocked on all 5 supported regions, GitHub Pages approved as substitute by Professor Ali Ziyaei (June 22, 2026)

In Progress:

* Frontend hosted via GitHub Pages — Azure Static Web Apps blocked on all 5 supported regions, GitHub Pages approved as substitute by Professor Ali Ziyaei (June 22, 2026)

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

The project has completed infrastructure provisioning, frontend connection, the live `submit_order` endpoint, queue-triggered validation, inventory stock checks, fan-out processing, Azure Table Storage logging, Azure Communication Services confirmation and rejection emails, Key Vault-backed secret handling, Managed Identity access, monitoring configuration, and Phase 8 end-to-end testing. Frontend is hosted via GitHub Pages — Azure Static Web Apps was blocked on all 5 supported regions under the Azure for Students subscription; GitHub Pages was approved as a substitute by Professor Ali Ziyaei (June 22, 2026).

Development is being completed in multiple phases, with the repository updated regularly to reflect architecture, implementation progress, testing evidence, and deployment artifacts.

### Project Status

**Current Phase:** Phase 8 Complete — Live on Azure

#### Progress Overview

* ✅ Project proposal approved
* ✅ Logical architecture completed
* ✅ Initial GitHub repository established
* ✅ Team collaboration workflow established
* ✅ Initial planning documentation completed
* ✅ Infrastructure architecture design
* ✅ Azure resource deployment
* ✅ Frontend implementation connected to live Function App endpoint
* ✅ `submit_order` Azure Function implemented and verified
* ✅ `validate_order` queue-triggered function implemented and verified
* ✅ `LaptopInventory` table integrated for stock checks and decrement logic
* ✅ `log_to_table` table logging function implemented and verified
* ✅ `send_confirmation_email` Azure Communication Services function implemented and verified
* ✅ `send_rejection_email` Azure Communication Services function implemented and verified
* ✅ Key Vault and Managed Identity security hardening completed
* ✅ Monitoring and observability configuration completed
* ✅ Phase 8 test matrix completed across six order scenarios
* ✅ Frontend hosting via GitHub Pages — approved by Professor Ali Ziyaei (June 22, 2026) as substitute for Azure Static Web Apps (blocked on all supported regions under Azure for Students subscription)

### Live Project Pages

* [Project roadmap](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/roadmap/project-roadmap-build-plan.html)
* [Architecture overview](https://rahatislamanik-spec.github.io/Azure-Event-Driven-Serverless-Order-Processing-System/architecture/project-architecture-overview.html)

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


