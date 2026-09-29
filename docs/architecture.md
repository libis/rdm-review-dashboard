<a href="https://libis.github.io/rdm-review-dashboard/"><button>Overview</button></a> <a href="https://libis.github.io/rdm-review-dashboard/installation.html"><button>Installation</button></a> <a href="https://libis.github.io/rdm-review-dashboard/architecture.html"><button>Architecture</button></a> 

<a href="https://libis.github.io/rdm-review-dashboard/backend.html"><button>Backend</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-review-dashboard.html"><button>Frontend Review Dashboard</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-check-my-dataset.html"><button>Frontend Check My Dataset</button></a>

<a href="https://libis.github.io/rdm-review-dashboard/roles.html"><button>Roles</button></a> <a href="https://libis.github.io/rdm-review-dashboard/checks.html"><button>Checks</button></a> <a href="https://libis.github.io/rdm-review-dashboard/emails.html"><button>Emails</button></a> <a href="https://libis.github.io/rdm-review-dashboard/review-workflow.html"><button>Review workflow</button></a> 

# Architecture

The review dashboard is a web application that supports dataset review, feedback, and curation workflows for Dataverse repositories.

The platform can optionally be extended with Check My Dataset, a self-service validation application that allows researchers to assess draft datasets before review or publication.

The platform consists of:

- Shared backend services (Python)
- Review Dashboard frontend (Angular)
- Check My Dataset frontend (Angular)
- Dataverse integrations
- A configurable review and feedback framework
- An shared automated validation (autocheck) framework

Both applications use the same backend infrastructure and validation framework, but provide different user experiences:

- Review Dashboard supports review workflows, dataset curation, and contributor feedback.
- Check My Dataset supports self-service dataset validation and quality improvement.



## System architecture

The platform integrates with several Dataverse components.


```text
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
```

### Dataverse

Dataverse serves as the system of records for datasets, metadata and permissions.

The Review Dashboard does not replace Dataverse workflows; instead, it adds structured review and feedback functionality on top of existing Dataverse functionality.

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

The backend can also serve the frontend applications as static content.

More information, see: [Backend](backend.md)

### Review Dashboard Frontend

The Review Dashboard frontend provides:

- Overview of the datasets in review
- Assignment management
- Review checklist
- Review notes
- Feedback interface
- Administrative functionality

It communicates exclusively with the backend.

More information, see: [Frontend Review Dashboard](frontend-review-dashboard.md)

### Check My Dataset Frontend

The Check My Dataset frontend provides:

- Dataset validation
- Overview of detected issues
- Complete validation results
- Recommendations for improving dataset quality

It communicates exclusively with the backend.

More information, see: [Frontend Check My Dataset](frontend-check-my-dataset.md)


## Review workflow

The Review Dashboard supports the following review workflow:


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


## Check My Dataset workflow

Check My Dataset enables researchers to evaluate datasets before they enter a formal review process.

```text
Researcher
     │
     ▼
Select dataset
     │
     ▼
Run validation checks
     │
     ▼
Overview of issues
     │
     ▼
All autocheck results
     │
     ▼
Tips to improve dataset
     │
     ▼
Dataset improvements
```

## Validation and review framework

The shared validation framework is driven by issue definitions and autocheck scripts. 

- Review Dashboard uses these components to support review workflows and feedback generation.
- Check My Dataset uses the same validation framework to present validation results and recommendations directly to dataset contributors.
 
A single autocheck script can be reused by both applications.

For a detailed description of the configuration of checks and feedback, see: [Checks](checks.md). 

### Review Dashboard

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

Selected review issues are automatically converted into dataset feedback and incorporated into configurable email templates. More information, see: [Emails](emails.md).

### Check My Dataset


```text
Issue Definition
       │
       ▼
Autocheck Script
       │
       ▼
Automatic Evaluation
       │
       ▼
Dataset Recommendations
```

## 4. Authentication and authorization

Neither the Review Dashboard nor Check My Dataset manage authentication themselves.

Authenticated user information is retrieved from HTTP request headers configured in the backend. User permissions are derived from Dataverse permissions and role mappings.

For details about role configuration and permission mapping, see: [Roles](roles.md).



