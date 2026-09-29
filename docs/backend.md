<a href="README.md"><button>Overview</button></a> <a href="installation.md"><button>Installation</button></a> <a href="architecture.md"><button>Architecture</button></a> <a href="frontend-review-dashboard.md"><button>Frontend Review Dashboard</button></a> <a href="frontend-check-my-dataset.md"><button>Frontend Check My Dataset</button></a>

<a href="roles.md"><button>Roles</button></a> <a href="checks.md"><button>Checks</button></a> <a href="emails.md"><button>Emails</button></a> <a href="review-workflow.md"><button>Review workflow</button></a>

# Backend configuration

## Overview

The backend provides services for both the Review Dashboard and Check My Dataset and integrates with Dataverse services.

The backend:

- Retrieves dataset information from Dataverse
- Accesses the Dataverse PostgreSQL database
- Retrieves data from the Solr index
- Uses the Dataverse Native API for dataset state changes
- Provides the API consumed by the Review dashboard and Check My Dataset frontends
- Manages review workflows, reviewer assignments, and review state
- Generates structured feedback and email notifications for the Review Dashboard

The backend is implemented in Python and is currently tested with Python 3.8.


## Configuration file

The backend is configured through a 'backend_config.json' file.

By default, the application expects this file in the root directory. The location can alternatively be specified through the 'BACKEND_CONFIG_FILE' environment variable.


## Backend configuration structure

The configuration file contains settings for:

- Dataverse integration
- Solr integration
- PostgreSQL connectivity
- SMTP configuration
- User and role management
- Application paths
- Validation and review configuration

### Dataverse related fields:
```
  "DataverseURL": URL of your installation, used for generating links to datasets.
  "DataverseAPI": URL of native API (without /api).
  "DataverseAPIKeyFile": Location of the file containing Dataverse API key.
```
   
### Solr related fields:
```
  "SolrHost": URL of the Solr index.
  "SolrAPIKeyFile": Location of the API key for Solr, if necessary.
```
  
### PostgreSQL related fields:
```
  "PostgresHost": PostgreSQL database host address.
  "PostgresPort": Port of the PostgreSQL database.
  "PostgresDB": Name of the Dataverse database in PostgreSQL.
  "PostgresUser": Username of the user that can access the PostgreSQL database. 
  "PostgresPasswordFile": Path of the file containing PostgreSQL database. 
```

### SMTP settings:
```
  "SMTPHost": SMTP host to be used for sending emails. 
  "SMTPPort": SMTP port.
  "SMTPPasswordFile": Password file. 
  "testEmail": If not null, all emails will be sent to this address.
  "helpdeskEmails": Email address of the helpdesk of your installation. Support request emails will be sent to this address.
```

### User related fields:
```
  "userIdHeaderField": The HTTP header field that contains the dataverse username of the reviewer. 
  "reviewerRoles": The user groups that can access the Review Dashboard. 
  "dataverseUserGroupAliases": The groups that can review datasets and admin the Review Dashboard.
```

More details about roles and permissions: [Roles](roles.md)
      
### Various paths:
```
  "UIPath": The path for the compiled UI files to be statically served by the backend. Set this to _null_ if you do not want the UI to be statically served by the backend.  
  "issueDefinitionsFile": Location of the dataset_issue_definitions.json, as described below.
  "emailTemplatesPath": Location of the template for feedback email, described below.
```

Issue definitions, more details: [Checks](checks.md).

More details about email templates, see [Emails](emails.md).

