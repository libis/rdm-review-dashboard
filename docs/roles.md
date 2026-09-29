<a href="https://libis.github.io/rdm-review-dashboard/"><button>Overview</button></a> <a href="https://libis.github.io/rdm-review-dashboard/installation.html"><button>Installation</button></a> <a href="https://libis.github.io/rdm-review-dashboard/architecture.html"><button>Architecture</button></a> 

<a href="https://libis.github.io/rdm-review-dashboard/backend.html"><button>Backend</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-review-dashboard.html"><button>Frontend Review Dashboard</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-check-my-dataset.html"><button>Frontend Check My Dataset</button></a>

<a href="https://libis.github.io/rdm-review-dashboard/roles.html"><button>Roles</button></a> <a href="https://libis.github.io/rdm-review-dashboard/checks.html"><button>Checks</button></a> <a href="https://libis.github.io/rdm-review-dashboard/emails.html"><button>Emails</button></a> <a href="https://libis.github.io/rdm-review-dashboard/review-workflow.html"><button>Review workflow</button></a> 

# Roles and permissions

## Overview

The Review Dashboard and Check My Dataset support role-based access control to ensure that users can only access datasets for which they have the appropriate permissions.

Rather than maintaining a separate permission model, both applications build on existing Dataverse roles and permissions. User access is determined through Dataverse role assignments and configurable role mappings.


## Access model

Access to datasets is based on the permissions a user already has in Dataverse. As a general principle, users can only access datasets that they are permitted to view or manage in Dataverse itself.

Typical examples include:

- Dataset contributors accessing their own datasets through Check My Dataset.
- Curators and reviewers accessing datasets assigned to them or available for review through the Review Dashboard.
- Repository administrators overseeing all datasets within their repository.

## Roles in Review Dashboard

The review dashboard provides two primary roles:

- Reviewer
- Administrator

These roles correspond to existing Dataverse roles and can be mapped through the application configuration. 


| Review dashboard role | Dataverse role |
|----------------------|----------------|
| Reviewer | Curator |
| Administrator | Admin |

Actual mappings are configurable and may vary between installations.


### Reviewer

The reviewer role corresponds to the Dataverse Curator role.

Reviewers perform the day-to-day review of datasets:

- Viewing datasets submitted for review
- Assigning datasets to themselves
- Completing review checklists
- Running and reviewing autocheck results
- Adding review notes
- Generating reviewer feedback
- Returning datasets for revision
- Publishing reviewed datasets


### Administrator

The administrator role corresponds to the Dataverse Admin role.

Administrators have all Reviewer capabilities and additional permissions required to manage and oversee the review process.

Typical administrator activities include:

- Taking over reviews from other reviewers
- Managing exceptional review situations
- Handling repository-level administrative tasks

## Roles in Check My Dataset

Check My Dataset does not introduce additional application-specific roles. Users can access datasets in Check My Dataset when they have sufficient permissions on those datasets in Dataverse. In most cases, this includes:

- Dataset contributors working on their own datasets
- Curators and reviewers who already have access to the dataset through Dataverse.

The exact set of accessible datasets therefore depends on the permissions granted within Dataverse.

## Authentication

Neither the Review Dashboard nor Check My Dataset manage authentication themselves.

Authenticated user information is obtained from HTTP request headers provided by the surrounding authentication infrastructure.

Once authenticated, users are assigned permissions based on their Dataverse group membership and configured role mappings.

For more information, see:

- [Backend](backend.md)
- [Architecture](architecture.md)
