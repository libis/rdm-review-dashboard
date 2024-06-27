# Review Dashboard Backend Configuration
## backend_config.json
The backend_config.json file contains settings for Review Dashboard backend. Its location can be set in the environment variable BACKEND_CONFIG_FILE. It contains the following fields:
  ### Dataverse related fields:
      "DataverseURL": URL of your installation, used for generating links to datasets.
      "DataverseAPI": URL of native API (without /api).
      "DataverseAPIKeyFile": Location of the file containing Dataverse API key.
    
  ### Solr related fields:
      "SolrHost": URL of the Solr index
    	"SolrAPIKeyFile": Location of the API key for Solr, if necessary. 

  ### PostgreSQL related fields:
      "PostgresHost": PostgreSQL database host address.
      "PostgresPort": Port of the PostgreSQL database.
      "PostgresDB": Name of the Dataverse database in PostgreSQL.
      "PostgresUser": Username of the user that can access the PostgreSQL database. 
      "PostgresPasswordFile": Path of the file containing PostgreSQL database. 

  ### SMTP settings:
      "SMTPHost": SMTP host to be used for sending emails. 
      "SMTPPort": SMTP port.
      "SMTPPasswordFile": Password file. 
      "testEmail": If not null, all emails will be sent to this address.
      "helpdeskEmails": Email address of the helpdesk of your installation. Support request emails will be sent to this address.

  ### User related fields:
      "userIdHeaderField": The HTTP header field that contains the dataverse username of the reviewer. 
      "reviewerRoles": The user groups that can access the Review Dashboard. 
      "dataverseUserGroupAliases": 
          "reviewer": 
          "admin": 
      
  ### Various paths:
      "UIPath": The path for the compiled UI files to be statically served by the backend. Set to _null_ if you do not want the UI to be statically served by the backend.  
      "issueDefinitionsFile": Location of the dataset_issue_definitions.json, described below.
	    "emailTemplatesPath": Location of the template for feedback email, described below.


## Issue Definitions and Feedback
The dataset_issue_definitions.json file contains the issues that the reviewers need to check in the review process for your installation. This file is also used in automatically generating feedback emails to be sent when datasets are returned to the author. 

Each issue has the following structure:
```
  "unique_id":  { 
    "category": "issue_category_to_group_issues",
    "id": "same_as_unique_id",
    "title": "Issue Name",
    "condition": "Condition that the dataset needs to meet to NOT have this issue. Reviewer will see this in the checklist and check it if the dataset passes this.",
    "warning": "Description of the status of the dataset that HAS the issue. Reviewers will see this in the summary of the issues at the end of the review.",
    "message": "The message that will be added to the feedback email to the dataset contributor. This field can contain HTML tags, such as links to relevant documentation for the dataset creators."
  }, 
```

An example:
```
  "readme":  { 
    "category": "files", // This issue belongs to the 'files' category
    "id": "readme", // Has the unique id of 'readme'
    "title": "Readme", 
    "condition": "README.txt or README.md file is present", // Ideally the dataset WILL contain a README.txt or README.md file. 
    "warning": "A README.txt or README.md file is missing.", // This will be displayed if this is not ticked. 
    "message": "A README.txt or README.md file is missing. For more information go to <a href=\"https://www.kuleuven.be/rdm/en/guidance/documentation-metadata/README\">https://www.kuleuven.be/rdm/en/rdr/manual#Documentation</a>" // This will be added to the feedback email. 
  }, 
```
This issue will appear as follows in the checklist for reviewer:
![alt text](docs/images/checklist.png)

And will be added to the review summary as the item 1:
![alt text](docs/images/review_issues_summary.png)

Will result in the following item in the feedback email:
![alt text](docs/images/feedback_email.png)

## Email Templates
The feedback email is sent to the dataset contact. The text for the email can be changed by editing feedback.txt in the path configured as emailTemplatesPath in backend_config.json. The following fields will be replaced when creating the actual email:
```
{author_names}
```
will be replaced with the first names of all authors. 

```
{dataset_title}
```
will be replaced by the actual title of the dataset. 

```
{issues_list}
```
will be replaced by a list of the issues the dataset has, based on the checklist modified by the reviewer. The list is enumerated for easy reference during correspondence with the dataset contact. 

```
{reviewer_name}
```
First name of the currently assigned reviewer. 

Note that, while this template constitutes the basis for the automatically generated feedback email, it can be edited and regenerated in the Review Dashboard UI during the review. The edited version will be automatically saved.