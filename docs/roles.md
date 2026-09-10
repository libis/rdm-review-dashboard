# Roles and permissions

## Overview

The review dashboard supports role-based access control to ensure that review activities can be performed by authorized users.

Rather than maintaining a separate permission model, the review dashboard builds on existing Dataverse roles and permissions. User access is determined through Dataverse role assignments and configurable role mappings in the dashboard.


## Role model

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



## Authentication

The Review Dashboard does not manage authentication itself.

Authenticated user information is obtained from HTTP request headers provided by the surrounding authentication infrastructure.

Once authenticated, users are assigned permissions based on their Dataverse group membership and configured role mappings.

For more information, see:

- [Backend](backend.md)
- [Architecture](architecture.md)
