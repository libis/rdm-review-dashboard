![RDR-logo](images/RDR-logo.png)

<a href="https://libis.github.io/rdm-review-dashboard/"><button style="background-color:#147fa1; color:white; border:none; border-radius:8px; padding:8px 14px;">Overview</button></a> <a href="https://libis.github.io/rdm-review-dashboard/installation.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Installation</button></a> <a href="https://libis.github.io/rdm-review-dashboard/architecture.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Architecture</button></a> <a href="https://libis.github.io/rdm-review-dashboard/backend.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Backend</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-review-dashboard.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Frontend Review Dashboard</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-check-my-dataset.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Frontend Check My Dataset</button></a>

<a href="https://libis.github.io/rdm-review-dashboard/roles.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Roles</button></a> <a href="https://libis.github.io/rdm-review-dashboard/checks.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Checks</button></a> <a href="https://libis.github.io/rdm-review-dashboard/emails.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Emails</button></a> <a href="https://libis.github.io/rdm-review-dashboard/review-workflow.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Review workflow</button></a> 

# Review Dashboard
## Introduction

The **Review Dashboard** is web application that aims to streamline the review, feedback and curation of datasets in Dataverse. It enables the installations to provide a standardized roadmap for their reviewers and keep track of datasets in various stages of the curation process. It provides reviewer assignment, configurable review checklists, automated quality checks, review notes and automated feedback generation, allowing reviewers to efficiently assess datasets before publication. It also maintains review state and reviewer comments, enabling continuity when reviews are reassigned.

The platform can be extended with **Check My Dataset**, a complementary self-service application that allows researchers to perform an initial automated assesssment of draft datasets before submission for review or curation. Check My dataset can be deployed together with the Review Dashboard as part of an integrated quality assurance workflow, or as a standalone aplication.

Both applications share the same backend infrastructure, configuration framework, and automated validation scripts. Validation checks can therefore be reused across both tools, ensuring consistent validation throughout the curation process.

A demonstration of the Review Dashboard is available [here](https://kuleuven.mediaspace.kaltura.com/media/KU+Leuven+Review+DashboardA+screen+recording/1_fuuts6ic).

[GitHub repository](https://github.com/libis/rdm-review-dashboard)

## Features

### Review Dashboard

- Overview of datasets awaiting review
- Reviewer assignment workflow
- Configurable review checklists
- Automated checks
- Review notes and reviewer handover support
- Automated feedback generation
- Role-based access management through Dataverse groups
- Configurable branding, feedback templates and review criteria

### Check My Dataset

- Self-service dataset validation for researchers
- Automated checks
- Overview of detected issues and warnings
- Complete overview of all validation results
- Dataset quality recommendations and improvement tips
- Reuse of the same validation logic as the Review Dashboard

## Current scope and limitations

The Review Dashboard is currently designed for Dataverse installations consisting of a single repository or collection.

Support for multi-institutional or multi-collection review workflows is currently not available. Installations that manage multiple independent repositories may require additional customization or future enhancements.


## Architecture

The Review Dashboard & Check My Dataset integrate with Dataverse and combines metadata retrieval and automated validation. Both tools share a common backend and automated validation framework.


                    Dataverse
         ┌────────────┼────────────┐
         │            │            │
    PostgreSQL      Solr      Native API
         │            │            │
         └────────────┴────────────┘
                      │
                      ▼
                Shared Backend
                │            |
                ▼            ▼
     Review Dashboard    Check My Dataset


For a detailed architectural overview, see:

- [Architecture](architecture.md)


## Quick start

See: [Installation](installation.md)

1. Clone the repository
2. Configure the backend
3. Build the frontend
4. Start the application


## Configuration and customization

The Review Dashboard and Check My Dataset share a common infrastructure and validation framework. Depending on the deployment, installations can use either application independently or deploy both applications together.

### Shared components

| Component | Configurable elements | Documentation |
|------------|------------|------------|
| Dataverse integration | Dataverse URL, Native API, API key | [Backend](backend.md) |
| Solr integration | Solr host, API key | [Backend](backend.md) |
| PostgreSQL integration | Host, port, database, user credentials | [Backend](backend.md) |
| Authentication | HTTP header containing authenticated user information | [Backend](backend.md) |
| Roles and permissions | Dataverse role mappings and access control | [Roles](roles.md) |
| Automated checks | Validation logic, warning generation, custom validation scripts | [Checks](checks.md) |

### Components Review Dashboard

| Component | Configurable elements | Documentation |
|------------|------------|------------|
| Frontend | Dataverse name, Dataverse URL, backend API URL | [Frontend Review Dashboard](frontend-review-dashboard.md) |
| Review checklist | Categories, checklist items, reviewer instructions, warning messages, contributor feedback messages | [Checks](checks.md) |
| Feedback generation | Mapping between checklist issues and contributor feedback | [Checks](checks.md) |
| Email delivery | SMTP server & credentials, helpdesk email addresses, test email address | [Backend](backend.md)
| Feedback emails | Email templates, placeholders, and default email content | [Emails](emails.md) |

### Components Check My Dataset

| Component | Configurable elements | Documentation |
|------------|------------|------------|
| Frontend | Dataverse name, Dataverse URL, backend API URL | [Frontend Check My Dataset](frontend-check-my-dataset.md) |
| Validation results | Overview messages, result descriptions, display rules, and recommendations | [Checks](checks.md) |
| Tips and recommendations | Guidance shown in the *Overview* and *General tips to improve your dataset* sections | [Checks](checks.md)


## Documentation

### Getting started

- [Installation](installation.md)
- [Architecture](architecture.md)

### Configuration

- [Backend](backend.md)
- [Frontend Review Dashboard](frontend-review-dashboard.md)
- [Frontend Check My Dataset](frontend-check-my-dataset.md)
- [Roles](roles.md)
- [Emails](emails.md)
- [Checks](checks.md)

### End-user guide

- [Review workflow](review-workflow.md)
- [User guide Check My Dataset](https://www.kuleuven.be/rdm/en/rdr/check-my-dataset-tool)

## Acknowledgement

This project was developed with support from KU Leuven and FOSB. We would like to thank all contributors and reviewers who provided valuable feedback throughout the design, implementation, and testing of the Review Dashboard.

## License

This project is licensed under the Apache 2.0 License.
