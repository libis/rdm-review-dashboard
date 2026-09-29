# Check My Dataset Frontend

The frontend requires a running backend and is built using Angular CLI  14.1.2. The frontend communicates exclusively with the backend API and cannot function independently. 


## Usage
Check my Dataset provides researchers with an early assessment of potential issues in their dataset using the same automated validation framework that powers the Review Dashboard. User needs to be logged on through their institutional logins to access the Check My Dataset tool. 

A user selects a dataset and starts a validation run. The frontend displays:

- Dataset information
- validation progress
- Validation results
- Detailed issues and recommendations


## Frontend configuration

The frontend is configured through: scr/assets/settings.json

The following configuration properties are available:

- ```"dataverseUrl"```: URL of your dataverse installation. It is used to produce the links to datasets. 
- ```"apiURL"```: address of the Review Dashboard backend API. 
- ```"dataverseName"```: name of your installation. By default it's set to 'Dataverse.'


## User access

Users without the required permissions cannot access the review dashboard. More information, see: [Roles](roles.md).


## User interface overview

After selecting a dataset, the validation results are presented in three sections:

- Overview
- All autocheck results
- General tips to improve your dataset

### Overview

Highlights items that require attention before publication. For each topic, you will find a short explanation together with links to guidance and practical instructions. The items are based on the **check_my_dataset_issue_definitions.json** in the backend, an autocheck is linked to each item.

### All autocheck results

This section provides a complete overview of all automated checks that were performed. By default, this section is hidden to keep the page concise.

### General tips to improve your dataset

Some important aspects of dataset quality cannot currently be assessed automatically. This section provides additional recommendations based on FAIR principles and repository best practices, with guidance and practical instructions for each topic. 

The items are based on the **check_my_dataset_issue_definitions.json** in the backend.


