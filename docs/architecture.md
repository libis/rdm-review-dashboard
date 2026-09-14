# Architecture

The review dashboard is a web application that supports dataset review, feedback, and curation workflows for Dataverse repositories.

The application consists of:

- A frontend (Angular)
- A backend (Python)
- Dataverse integrations
- A configurable review and feedback framework
- An automated validation ("autocheck") framework

The dashboard retrieves dataset information from Dataverse, allows reviewers to assess datasets using configurable review criteria, and generates structured feedback for dataset contributors.


## 1. System architecture

The review dashboard integrates with several Dataverse components.


```text
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
```

### Dataverse

Dataverse serves as the system of records for datasets, metadata and permissions.

The review dashboard does not replace Dataverse workflows; instead, it adds structured review and feedback functionality on top of existing Dataverse functionality.

### PostgreSQL

The backend accesses the Dataverse PostgreSQL database to retrieve dataset and repository information efficiently.

### Solr

Solr is used for fast retrieval and indexing of dataset information.

### Dataverse native API

Operations that modify dataset state, such as returning datasets for revision and publication actions, use the Dataverse Native API.

### Backend

The backend provides

- Dataset retrieval
- Review workflow management
- Reviewer assignment
- Role management
- Autocheck execution
- Feedback generation

The backend can also serve the frontend as static content.

More information, see: [Backend](backend.md)

### Frontend

The frontend provides:

- Overview of the datasets in review
- Assignment management
- Review checklist
- Review notes
- Feedback interface
- Administrative functionality

It communicates exclusively with the backend.

More information, see: [Frontend](frontend.md)


## 2. Review workflow

The review dashboard supports the following review workflow:


```text
Researcher
     │
     ▼
Submit dataset for review
     │
     ▼
Dataset appears in review queue
     │
     ▼
Reviewer assignment
     │
     ▼
Review checklist
     │
     ▼
Autocheck execution
     │
     ▼
Manual review
     │
     ▼
Feedback generation
     │
     ▼
Return for revision
            or
         Publish
```

More information, see: [Review workflow](review-workflow.md)


## 3. Review framework architecture


The review workflow is driven by a set of configurable definitions and scripts that determine how datasets are evaluated and how feedback is generated.

```text
Issue Definition
       │
       ▼
Review Checklist
       │
       ▼
Reviewer Evaluation
       │
       ▼
Feedback Generation
       │
       ▼
Feedback Email

Optional:

Autocheck Script
       │
       ▼
Automatic Evaluation
```


For a detailed description of the configuration of checks and feedback, see: [Checks](checks.md). 

Selected review issues are automatically converted into dataset feedback and incorporated into configurable email templates. More information, see: [Emails](emails.md).



## 4. Authentication and authorization

The review dashboard relies on the surrounding authentication infrastructure.

Authenticated user information is retrieved from HTTP request headers configured in the backend.

For details about role configuration and permission mapping, see: [Roles](roles.md)



