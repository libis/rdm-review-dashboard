# Review Dashboard
## Introduction
The Review Dashboard is a web application that aims to streamline the review, feedback and curation of datasets in Dataverse. It enables the installations to provide a standardized roadmap for their reviewers, streamline their review and feedback process, and keep track of datasets in various stages of the curation process. It keeps state of the review checklist, feedback emails composed based on it, and review notes, which can be accessed by the reviewer assigned to the dataset, which makes it useful in case of a reviewer change. 

The dashboard connects to Dataverse via PostgreSQL and Solr for fast retrieval of dataverse and dataset information, and uses the Dataverse Native API for reviewer assignments and status changes (publish/return) to ensure safety. It integrates into your authentication system by getting the current authenticated username from HTTP headers. Access rights are controlled using dataverse user groups, by adding users to reviewer and admin groups in the Dataverse UI.
It allows for various customization options, with customizable repository name, review checklists, and feedback emails. Branding can be customized by placing custom header and footer HTMLs. The Dataverse user group names can also be customized to integrate or not conflict with installations’ existing groups. 

## Installation
The review dashboard contains a frontend and a backend. The frontend requires Angular CLI 14.1.2 to build. 
At the runtime, the app requires a backend_config.json file, which should by default be placed to the default location in the root directory. Alternatively, it’s location can be set in BACKEND_CONFIG_FILE environment variable, which can be useful when running from a container.  For more in-depth please refer to the the configuration files.

To build the frontend, navigate to the rdm-review-dashboard-backend directory and run:
```
make build-frontend
```

After building the frontend, you can run the dashboard by running rdm-review-dashboard-backend/src/main.py  with Python 3:
```
python rdm-review-dashboard-backend/src/main.py  
```

This will also statically serve the frontend, if the UI_PATH variable is set. If you do not want the frontend to be served by the backend (to put it into a separate container or serve it otherwise), set UI_PATH to null. For more in-depth look at the configuration, see [ ].

To build the Review Dashboard as a Docker container, after building the frontend, use;
```
make build-container
```
and to run locally:
```
make run
```

The container could be added to your Docker Compose setup by using the compose.review.yml. For example, to try the review dashboard with the Dataverse demo container, download the Dataverse demo compose.yml from Dataverse container [Demo or Evaluation page] (https://guides.dataverse.org/en/latest/container/running/demo.html) into the root folder and in the root folder run:
```
docker compose -f compose.yml -f compose.review.yml up
```

## Configuration
The frontend and the backend are configured separately. Please see their configuration documentations. 