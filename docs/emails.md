# Feedback emails

## Overview

The review dashboard can automatically generate feedback emails when a dataset is returned to the contributor for revision.

The generated feedback is based on:

- the configured issue definitions;
- the issues selected by the reviewer;
- the email template configuration.


```text
Issue Definitions
        │
        ▼
Selected Review Issues
        │
        ▼
Feedback Generation
        │
        ▼
Email Template
        │
        ▼
Feedback Email
```

The automatically generated email can be edited by the reviewer before it is sent.


## Email template

The text of the email can be changed by editing feedback.txt in the path configured as emailTemplatesPath in backend_config.json. The following fields will be replaced when creating the actual email:
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

## Editing feedback emails

The feedback template serves as the basis for automatically generated feedback emails.

Reviewers can further edit the generated email directly in the review dashboard during the review process. 