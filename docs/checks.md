# Checks and feedback

## Overview

The review dashboard uses a configurable checklist to support dataset review.

Each checklist item is defined as an **issue**. Issues can be reviewed manually by a reviewer or evaluated automatically through an **autocheck**.

In addition to driving the review workflow, issue definitions are also used to generate structured feedback for dataset contributors when datasets are returned for revision.


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

Optional:

Autocheck Script
       │
       ▼
Automatic Evaluation
```

## Review framework architecture

The review framework consists of several components that work together to evaluate datasets and generate feedback.

```text
Issue Definition
       │
       ▼
Review Checklist
       │
       ├── Manual Review
       │
       └── Automatic Review
                │
                ▼
         Autocheck Script
                │
                ▼
         Autocheck Result
       │
       ▼
Review Summary
       │
       ▼
Feedback Email
```

The issue definition is the central configuration component. It determines:

- which checks are show in the review checklist;
- how issues are grouped;
- which texts are displayed to reviewers;
- which feedback is sent to dataset contributors.

Autochecks can optionally be linked to issue definitions to assist reviewers by automatically evaluating specific requirements.


## Issue Definitions

Issue definitions define the checklist items that reviewers use during the review process.

Configuration file: config/dataset_issue_definitions.json

Each issue appears as a checklist item in the review dashboard and can contribute to the automatically generated feedback when datasets are returned for revision.

### Structure


Each issue has the following structure:

```json
{
  "unique_id": {
    "category": "issue_category_to_group_issues",
    "id": "same_as_unique_id",
    "title": "Issue Name",
    "condition": "Condition that the dataset should meet",
    "warning": "Description shown when the issue is present",
    "message": "Feedback sent to dataset contributors"
  }
}
```

### Properties

#### category

Groups issues together in the review checklist.

Common categories include:

- files
- metadata
- terms

#### id

unique identifier of the issue.

This should match the issue name.

#### title

Human-readable title shown in the review checklist.

#### condition

Describes the expected situation.

The reviewer sees this text in the checklist and confirms it when the requirement is met.

#### warning

Describes the situation when the issue is present.

This text is shown in the review summary.

#### message

Detailed guidance for dataset contributors.

The message is automatically added to feedback emails when the issue is selected during review.

HTML tags may be used, including links to relevant documentation.

### Example


```json
{
  "readme": {
    "category": "files",
    "id": "readme",
    "title": "README",
    "condition": "README.txt or README.md file is present",
    "warning": "A README.txt or README.md file is missing.",
    "message": "A README.txt or README.md file is missing. For more information, see the README guidance..."
  }
}
```

### Checklist representation

The issue appears as a checklist item for reviewers.

images/checklist.png

### Review summary representation

Issues that are not resolved appear in the review summary.

images/feedback_email.png


## Manual and automatic checks

The review dashboard supports both manual and automatic checks.

### Manual checks

Manual checks require reviewer judgement and are evaluated directly by the reviewer.

Manual checks only require an issue definition.

### Automatic checks

Automatic checks use validation scripts to assist reviewers.


An automatic check consists of:

```text
Issue Definition
       │
       ▼
Autocheck Script
       │
       ▼
Autocheck Result
```

The reviewer remains responsible for the final review decision.

Autochecks support the review process but do not replace reviewer judgement.


## Autocheck scripts

Autocheck scripts perform the actual validation of dataset elements and metadata.

Location: rdm-review-dashboard-backend/src/autochecks


Each script is responsible for:

- executing validation logic;
- evaluating dataset content or metadata;
- generating validation results;
- generating warning messages.

Possible outcomes typically include:

- success
- warning
- failure

Warning messages displayed by the Review Dashboard originate from the autocheck scripts themselves.

Changes to warning messages therefore require modifications to the corresponding script.

### Script template

New autocheck scripts can be based on the provided template:

config/automations/template.py


```python
from autochecks.check import CheckResult, DatasetContext
from datetime import datetime

def run(context: DatasetContext) -> CheckResult:
    result: bool | None = None
    message: str | None = None
    return CheckResult(result, message, datetime.now())
```

Each autocheck script must implement a `run()` function that accepts a `DatasetContext` object and returns a `CheckResult`.

#### Dataset context

The 'DatasetContext' object provides access to information needed by the validation script.

Depending on the check, this can include:

- dataset metadata
- dataset files
- terms and permissions

#### Warning messages

The warning message provides additional information for reviewers.

Warning messages are displayed in the review dashboard and should clearly explain why the check did not pass. 


### Example

The example below checks whether a dataset contains a README file.


```python
from autochecks.check import CheckResult, DatasetContext
from utils.logging import logging
from datetime import datetime
import time

min_filesize = 15

readme_fnames = [
    "readme.txt",
    "readme.md",
    "00_readme.txt",
    "00_readme.md"
]

def get_files_with_name(files, namelist):
    result = []

    for file in files:
        fname = file.get("dataFile").get("filename")
        fsize = file.get("dataFile").get("filesize")
        restricted = file.get("restricted")

        if fname.lower() in namelist:
            result.append({
                "filename": fname,
                "filesize": fsize,
                "restricted": restricted
            })

    return result

def run(context: DatasetContext) -> CheckResult:
    result = None
    warning = ""

    readmes = get_files_with_name(
        context.files,
        readme_fnames
    )

    for file in readmes:
        if file.get("filesize") < min_filesize:
            warning += (
                f"{file.get('filename')} "
                f"has length < {min_filesize} characters.\n"
            )

    if warning == "":
        warning = None

    if not warning and len(readmes) == 1:
        result = True

    return CheckResult(result, warning)
```

### Existing autochecks

*Coming soon*


## Adding a new check

The process depends on whether the new check should be evaluated manually or automatically.

### Adding a manual check

1. Add a new issue definition to: dataset_issue_definitions.json
2. Verify that the checklist item appears correctly, the issue is displayed in the review summary, feedback generation works as expected

### Adding an automatic check

1. Add a new issue definition to: dataset_issue_definitions.json
2. Create the validation script
3. Verify that the autocheck result is correctly linked to the issue definition
4. Test checklist integration and feedback generation


## Writing guidelines

The following fields should remain aligned:

- title
- condition
- warning
- message

Good feedback messages should:

- explain why the issue matters;
- explain how researchers can resolve the issue;
- provide links to relevant guidance where appropriate.

Consistency between checklist text, warning text and feedback text improves reviewer efficiency and creates clearer feedback for contributors. 