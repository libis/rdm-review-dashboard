# Review Dashboard
## Introduction
The Review Dashboard is a web application that aims to streamline the review, feedback and curation of datasets in Dataverse. It enables the installations to provide a standardized roadmap for their reviewers and keep track of datasets in various stages of the curation process. It provides reviewer assignment, configurable review checklists, automated quality checks, review notes and automated feedback generation, allowing reviewers to efficiently assess datasets before publication. It also maintains review state and reviewer comments, enabling continuity when reviews are reassigned. 

A demonstration of the review dashboard is available here: https://kuleuven.mediaspace.kaltura.com/media/KU+Leuven+Review+DashboardA+screen+recording/1_fuuts6ic.


## Features

- Overview of datasets awaiting review
- Reviewer assignment workflow
- Configurable review checklists
- Automated checks
- Review notes and reviewer handover support
- Automated feedback generation
- Role-based access management through Dataverse groups
- Configurable branding, feedback templates and review criteria


## Current scope and limitations

The review dashboard is currently designed for Dataverse installations consisting of a single repository or collection.

Support for multi-institutional or multi-collection review workflows is not currently available. Installations that manage multiple independent repositories may require additional customization or future enhancements.


## Architecture

The review dashboard integrates with Dataverse and combines metadata retrieval, automated validation and review workflows.


                    Dataverse
         ┌────────────┼────────────┐
         │            │            │
    PostgreSQL      Solr      Native API
         │            │            │
         └────────────┴────────────┘
                      │
                      ▼
          Review Dashboard Backend
                      │
                      ▼
             Review Dashboard UI

   Autochecks → Results → Issues → Feedback

For a detailed architectural overview, see:

- [Architecture](architecture.md)


## Quick start

See: [Installation](installation.md)

1. Clone the repository
2. Configure the backend
3. Build the frontend
4. Start the application


## Configuration and customization

The review dashboard supports various customization options. The table below provides an overview of the main configurable components and where they are documented.

| Component | Configurable elements | Documentation |
|------------|------------|------------|
| Dataverse integration | Dataverse URL, Native API, API key | [Backend](backend.md) |
| Solr integration | Solr host, API key | [Backend](backend.md) |
| PostgreSQL integration | host, port, database, user credentials | [Backend](backend.md) |
| Email delivery | SMTP server & credentials, helpdesk email addresses, test email address | [Backend](backend.md) |
| Authentication | HTTP header containing authenticated user information | [Backend](backend.md) |
| Frontend | Dataverse name, URL, backend API URL | [Frontend](frontend.md) |
| Roles and permissions | Reviewer and administrator roles, Dataverse group mappings | [Roles](roles.md) |
| Review checklist | Categories, checklist items, reviewer instructions, warning messages, contributor feedback messages | [Checks](checks.md) |
| Automated checks | Validation logic, warning generation, custom validation scripts | [Checks](checks.md) |
| Feedback generation | Mapping between checklist issues and contributor feedback | [Checks](checks.md) |
| Feedback emails | Email templates, placeholders and default email content | [Emails](emails.md) |


## Documentation

### Getting started

- [Installation](installation.md)
- [Architecture](architecture.md)

### Configuration

- [Backend](backend.md)
- [Frontend](frontend.md)
- [Roles](roles.md)
- [Emails](emails.md)
- [Checks](checks.md)

### End-user guide for performing reviews

- [Review workflow](review-workflow.md)


## License

This project is licensed under the Apache 2.0 License.
