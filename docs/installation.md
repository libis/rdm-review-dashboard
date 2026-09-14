# Installation

This guide describes how to install and run the review dashboard.

The installation process consists of the following steps:

1. Preparing prerequisites
2. Clone the repository
3. Configure Dataverse permissions
4. Configure the backend
5. Configure authentication
6. Build the frontend
7. Start the application
8. Verify the installation
9. (optional) deploy using Docker
10. Continue with advanced configuration


## 1. Prerequisites

The review dashboard consists of a backend and a frontend. It integrates with an existing Dataverse installation and requires access to Dataverse services and metadata sources.

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

The review dashboard uses Dataverse groups to determine which users can access the application and perform reviews.

1. Create a reviewer group in Dataverse
2. Add reviewers to this group
3. Optionally create a separate administrator group
4. Configure the corresponding group aliases in the backend configuration

For more information, see: 

- [Roles](roles.md)


## 4. Configure the backend

The application requires a 'backend_config.json' file at runtime. By default, the file is expected in the application root directory. 
Alternatively, its location can be specified through the 'BACKEND_CONFIG_FILE' environment variable, which can be useful when running from a container.

Configure:

- Dataverse URL
- Dataverse API endpoint
- Authentication header ('userIdHeaderField')
- Reviewer and administrator role mappings
- Paths to application configuration files

For a complete description of all available configuration parameters, see:

- [Backend](backend.md)


## 5. Configure authentication

The dashboard obtains the authenticated user's identifier from an HTTP header supplied by the authentication infrastructure. 
The header field used for this purpose is configured through the backend configuration.

During development, browser plugins can be used to simulate this header for testing purposes.


## 6. Build the frontend

Build the Angular frontend using:


```bash
make build-frontend
```

For more information, see [Frontend](frontend.md)

## 7. Start the application

Run the application using:

```bash
make run
```

The backend can optionally serve the frontend as static content when the `UI_PATH` configuration parameter is set. If the frontend is hosted separately, set `UI_PATH` to `null`.


## 8. Verify the installation

After starting the application:

1. Open the review dashboard in a browser
2. Verify that authentication works
3. Verify that datasets are displayed
4. Verify that reviewer permissions are applied correctly
5. Verify that dataset assignment functionality is available
6. Verify that review checklists load correctly


## 9. (optional) Docker deployment

To build the review dashboard as a Docker container, after building the frontend, use:

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
- UI configuration
- Roles and permissions
- (Auto)check configuration
- Email template configuration

