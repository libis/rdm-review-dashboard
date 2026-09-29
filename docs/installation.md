<a href="https://libis.github.io/rdm-review-dashboard/"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Overview</button></a> <a href="https://libis.github.io/rdm-review-dashboard/installation.html"><button style="background-color:#147fa1; color:white; border:none; border-radius:8px; padding:8px 14px;">Installation</button></a> <a href="https://libis.github.io/rdm-review-dashboard/architecture.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Architecture</button></a> 

<a href="https://libis.github.io/rdm-review-dashboard/backend.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Backend</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-review-dashboard.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Frontend Review Dashboard</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-check-my-dataset.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Frontend Check My Dataset</button></a>

<a href="https://libis.github.io/rdm-review-dashboard/roles.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Roles</button></a> <a href="https://libis.github.io/rdm-review-dashboard/checks.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Checks</button></a> <a href="https://libis.github.io/rdm-review-dashboard/emails.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Emails</button></a> <a href="https://libis.github.io/rdm-review-dashboard/review-workflow.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Review workflow</button></a> 

# Installation

This guide describes how to install and run the Review Dashboard and, optionally, Check My Dataset.

Both applications share the same backend infrastructure and automated validation framework. Depending on your requirements, you can:

- Deploy the Review Dashboard only
- Deploy Check My Dataset only
- Deploy both applications together using a shared backend

The installation process consists of the following steps:

1. Preparing prerequisites
2. Clone the repository
3. Configure Dataverse permissions
4. Configure the backend
5. Configure authentication
6. Build the frontend application(s)
7. Start the application
8. Verify the installation
9. (optional) deploy using Docker
10. Continue with advanced configuration


## 1. Prerequisites

The platform consists of a shared backend and one or more frontend applications. It integrates with an existing Dataverse installation and requires access to Dataverse services and metadata sources.

Before installing, make sure you have:

- a running Dataverse installation
- access to the Dataverse PostgreSQL database
- access to the Dataverse Solr index
- access to the Dataverse Native API
- Python environment for the backend
- Angular CLI 14.1.2 for frontend builds
- Git
- Docker (optional, for container-based deployments)


## 2. Clone the repository

```bash
git clone https://github.com/libis/rdm-review-dashboard.git
cd rdm-review-dashboard
```


## 3. Configure Dataverse permissions

The exact permissions required depend on the deployed application.

For the Review Dashboard, Dataverse groups are used to determine which users can access the application and perform reviews.

1. Create a reviewer group in Dataverse
2. Add reviewers to this group
3. Optionally create a separate administrator group
4. Configure the corresponding group aliases in the backend configuration

For Check My Dataset, users can access datasets according to their existing Dataverse permissions.

For more information, see: 

- [Roles](roles.md)


## 4. Configure the backend

The application requires a 'backend_config.json' file at runtime. By default, the file is expected in the application root directory. 
Alternatively, its location can be specified through the 'BACKEND_CONFIG_FILE' environment variable, which can be useful when running from a container.

Configure:

- Dataverse URL
- Dataverse API endpoint
- Authentication header ('userIdHeaderField')
- Reviewer and administrator role mappings (Review Dashboard)
- Review Dashboard issue definition file
- Check My Dataset issue definition file
- Paths to application configuration files

For a complete description of all available configuration parameters, see:

- [Backend](backend.md)


## 5. Configure authentication

The dashboard obtains the authenticated user's identifier from an HTTP header supplied by the authentication infrastructure. 
The header field used for this purpose is configured through the backend configuration.

During development, browser plugins can be used to simulate this header for testing purposes.


## 6. Build the frontend

Build the Angualar frontend application(s) that you want to deploy using:


```bash
make build-frontend
```

For more information, see [Frontend Review Dashboard](frontend-review-dashboard.md).

For more information, see [Frontend Check My Dataset](frontend-check-my-dataset.md)

## 7. Start the application

Run the application using:

```bash
make run
```

The backend can optionally serve the frontend as static content when the `UI_PATH` configuration parameter is set. If the frontend is hosted separately, set `UI_PATH` to `null`.


## 8. Verify the installation

Verify the components that were deployed

### Review Dashboard

1. Open the Review Dashboard in a browser
2. Verify that authentication works
3. Verify that datasets are displayed
4. Verify that reviewer permissions are applied correctly
5. Verify that dataset assignment functionality is available
6. Verify that review checklists load correctly

### Check My Dataset

1. Open Check My Dataset in a browser
2. Verify that authentication works
3. Verify that accessible datasets are displayed
4. Verify that validation checks can be executed
5. Verify that validation results are displayed correctly
6. Verify that tips and recommendations appear as expected


## 9. (optional) Docker deployment

To build the Review Dashboard as a Docker container, after building the frontend, use:

```bash
make build-container
```

The container can be added to your Docker Compose by using the compose.review.yml. For example, to try the review dashboard with the Dataverse demo container, download the Dataverse demo compose.yml (https://guides.dataverse.org/en/latest/container/running/demo.html) into the root folder and in the root folder of the review dashboard run:
```
docker compose -f compose.yml -f compose.review.yml up
```


## 10. Continue with advanced configuration

Once the application is running, continue with:

- Architecture
- Backend configuration
- Review Dashboard Frontend configuration
- Check My Dataset Frontend configuration
- Roles and permissions
- Review Dashboard issue definitions
- Check My Dataset issue definitions
- Autocheck configuration
- Email template configuration

