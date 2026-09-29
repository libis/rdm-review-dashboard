<a href="https://libis.github.io/rdm-review-dashboard/"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Overview</button></a> <a href="https://libis.github.io/rdm-review-dashboard/installation.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Installation</button></a> <a href="https://libis.github.io/rdm-review-dashboard/architecture.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Architecture</button></a> 

<a href="https://libis.github.io/rdm-review-dashboard/backend.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Backend</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-review-dashboard.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Frontend Review Dashboard</button></a> <a href="https://libis.github.io/rdm-review-dashboard/frontend-check-my-dataset.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Frontend Check My Dataset</button></a>

<a href="https://libis.github.io/rdm-review-dashboard/roles.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Roles</button></a> <a href="https://libis.github.io/rdm-review-dashboard/checks.html"><button style="background-color:#147fa1; color:white; border:none; border-radius:8px; padding:8px 14px;">Checks</button></a> <a href="https://libis.github.io/rdm-review-dashboard/emails.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Emails</button></a> <a href="https://libis.github.io/rdm-review-dashboard/review-workflow.html"><button style="background-color:#00407A; color:white; border:none; border-radius:8px; padding:8px 14px;">Review workflow</button></a> 

# Checks and feedback

## Overview

The Review Dashboard and Check My Dataset use configurable issue definitions to evaluate datasets and present validation results. 

Both applications share the same autocheck framework and validation scripts, but use different issue definition files and present results in different ways:

- The Review Dashboard uses issue definitions to support dataset review and feedback generation.
- Check My Dataset uses issue definitions to present validation results and recommendations directly to dataset contributors.

The shared validation framework consists of:

- issue definitions
- autocheck scripts
- validation results

Issue definitions determine how validation results are presented in each application, while the underlying autocheck scripts remain shared.


## Review Dashboard workflow

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

## Check My Dataset workflow

```text
Issue Definition
│
├── Optional Autocheck Script
│             │
│             ▼
│      Validation Result
│
▼
Presentation Rules
│
├── Overview
│      └── Issues requiring attention
│          + associated guidance
│
├── All Autocheck Results
│      └── Complete list of validation results
│
└── Tips to Improve Your Dataset
       ├── Conditional tips based on autocheck results
       └── General recommendations without autochecks
```

In Check My Dataset, issue definitions determine:

- which validation scripts are executed;
- how validation results are presented;
- which guidance is shown to dataset creators;
- when recommendations appear in the user interface.

## Issue Definition files

The applications use separate issue definitions files.

### Review Dashboard issue definitions

Configuration file: config/dataset_issue_definitions.json

Issue definitions define the checklist items that reviewers use during the review process. Each issue appears as a checklist item in the Review Dashboard and can contribute to the automatically generated feedback when datasets are returned for revision.

#### Structure

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

#### Properties

**category**

Groups issues together in the review checklist.

Common categories include:

- files
- metadata
- terms

**id**

unique identifier of the issue. This should match the issue name.

**title**

Human-readable title shown in the review checklist.

**condition**

Describes the expected situation. The reviewer sees this text in the checklist and confirms it when the requirement is met.

**warning**

Describes the situation when the issue is present. This text is shown in the review summary.

**message**

Detailed guidance for dataset contributors. The message is automatically added to feedback emails when the issue is selected during review. HTML tags may be used, including links to relevant documentation.

#### Example


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

#### Representation in the user interface

**Checklist representation**

The issue appears as a checklist item for reviewers ([see screenshot](images/checklist.png))

**Review summary representation**

Issues that are not resolved appear in the review summary ([see screenshot](images/feedback_email.png)).


### Check My Dataset issue definitions

Configuration file: config/check_my_dataset_issue_definitions.json.

Each issue definition controls:

- how the issue is evaluated;
- how the issue is displayed;
- in which section(s) it appears;
- which autocheck script is associated with it (optionally).

#### Validation model

The Check My Dataset interface contains three sections:

- Overview
- All Autocheck Results
- General tips to improve your dataset

**Overview**

The **Overview** section highlights issues that require the user's attention.

An issue is displayed in this section when:

- the issue has an autocheck script;
- the autocheck result is **failure** or **warning**;
- an 'overview_header' has been configured.

Display logic:

- 'overview_header' is used as the default heading.
- If the autocheck returns a warning message, the warning message replaces the configured 'overview_header'
- if an autocheck cannot be evaluated and returns no result, the heading is replaced by: *This requirement could not be automatically validated, please check its correctness manually*.
- 'overview_content' is shown inside the accordion.
- If 'overview_content' is empty or omitted, the accordion is disabled and only the heading is displayed.

The purpose of this section is to provide a concise summary of all detected issues and warnings.

Because warning messages generated by autocheck scripts override the configured 'overview_header', issue definitions should be written so that the configured headers, warning messages, and explanatory content remain consistent when displayed together.

**All autocheck results**

The **All autocheck results** section contains every issue that had an autocheck script, regardless of the result.

For each issue:

- the autocheck result (success, failure, or warning) is displayed;
- 'all_results_header' is shown next to the result indicator.

Examples:

- "Dataset is smaller than 50GB"
- "README.txt or README.md file is present"

The purpose of this section is to provide a complete overview of all performed checks.

**General tips to improve your dataset**

The **General tips to improve your dataset** section contains additional guidance and recommendations.

Tips can be displayed:

- always;
- never;
- conditionally based on the result of an autocheck.

The display behaviour is controlled by the 'display_in_tips' property.

**Supported values**

| Value | Description |
|---------|-------------|
| `always` | Always display the tip |
| `never` | Never display the tip |
| `success` | Display only when the autocheck succeeds |
| `fail` | Display only when the autocheck fails |
| `warning` | Display only when the autocheck returns a warning |
| `fail_or_warning` | Display when the autocheck fails or returns a warning |

**Display logic**

- 'tips_header' is used as the accordion header.
- 'tips_content' is displayed when the accordion is expanded.
- If 'tips_content' is empty, the accordion is disabled an only the header is shown.

Issue definitions do not need to be linked to an autocheck script. When no script is configured, the issue can still be used to provide general recommendations in the General tips to improve your dataset section. This allows the application to present dataset quality guidance even for aspects that cannot currently be evaluated automatically. 

Examples include:

- handling personal data
- writing a dataset description

#### Structure

```json
{
  "category": "files",
  "script": "totalDatasetFilesSizeIsLessThan50GB",
  "title": "Dataset size",
  "overview_header": "Dataset is larger than 50 GB",
  "overview_content": "...",
  "all_results_header": "Dataset is smaller than 50 GB",
  "display_in_tips": "fail",
  "tips_header": "Dataset size",
  "tips_content": "..."
}
```

#### Properties

| Property | Description | Required | Comment |
|-----------|-------------|-----------|-------------|
| `category` | Determines under which category the issue is grouped | mandatory | Files, Metadata, Terms |
| `script` | The autocheck script associated with the issue | optional | can be omitted |
| `title` | Human-readable title of the issue | mandatory | appears in bold in Overview and Tips sections |
| `overview_header` | Default header shown in the Overview section | mandatory | no html possible |
| `overview_content` | Accordion content shown in the Overview section | recommended | html possible |
| `all_results_header` | Text displayed next to the check result | mandatory | appears in All results section |
| `display_in_tips` | Determines when the tip is displayed | mandatory | "always", "never", "success", "fail", "warning", "fail_or_warning" |
| `tips_header` | Header shown in the Tips section | mandatory if displayed in Tips | appears in bold, no html possible |
| `tips_content` | Content shown when the accordion is expanded | recommended if displayed in Tips | html possible |


## Manual and automatic checks

The platform supports both manual and automatic checks.

### Manual checks

Manual checks require reviewer judgement and are evaluated directly by the reviewer. 
Manual checks are only available in the Review Dashboard and require an issue definition.

### Automatic checks

Automatic checks use validation scripts to evaluate dataset content and metadata.

The automated validation framework is shared by the Review Dashboard and Check My Dataset, ensuring consistent validation results across both applications.


An automatic check consists of:

```text
Issue Definition
       │
       ▼
Autocheck Definition
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

**Important**

Autocheck scripts are shared components used by both the Review Dashboard and Check My Dataset. Changes to validation logic or warning messages may therefore affect both applications.

Each script is responsible for:

- executing validation logic;
- evaluating dataset content or metadata;
- generating validation results;
- generating warning messages.

Possible outcomes typically include:

- success
- warning
- failure

Warning messages are shared across the Review Dashboard and Check My Dataset.

In the Review Dashboard, warning messages are displayed when hovering the corresponding checklist item to provide additional context to reviewers.

In Check My Dataset:

- Warning messages override the configured 'overview_header' in the **Overview** section.
- Warning messages are displayed in the **All autocheck results** section.

Warning messages should therefore be understandable to both reviewers and dataset contributors and should clearly explain why the check did not pass.

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
4. Test the check in the Review Dashboard
5. If the check should (also) be available in Check My Dataset, add a corresponding entry to check_my_dataset_issue_definitions.json
6. Verify that all user-facing texts and warning messages are appropriate for both applications.


## Writing guidelines

The Review Dashboard and Check My Dataset use separate issue definition files, but they share the same validation framework. Content across both applications should therefore remain aligned and consistent.

### Review Dashboard

The following fields should remain aligned:

- title
- condition
- warning
- message


### Check My Dataset

The following fields should remain aligned:

- title
- overview_header
- overview_content
- all_results_header
- tips_header
- tips_content

### Alignment between applications

The Review Dashboard and Check My Dataset share the same autocheck scripts and warning messages.

Because the same warning text is reused in multiple contexts and for different audiences, warning messages should:
 
- be understandable to both reviewers and dataset contributors;
- clearly explain the detected issue;
- avoid repository-specific terminology where possible;
- remain consistent with the corresponding issue definition texts.

In Check My Dataset, warning messages can replace the configured `overview_header`. Therefore:
 
- `overview_header`
- `overview_content`
- `all_results_header`
- `tips_header`
- `tips_content`
- autocheck warning messages
 
should be written as a coherent set of messages that remains meaningful regardless of whether a warning is generated.

### Writing recommendations

User-facing texts should:

- clearly explain why the issue matters;
- explain how the issue can be resolved;
- use concise and actionable language;
- provide links to relevant guidance where appropriate.

Consistent wording across Review Dashboard checklists, validation results, warning messages, feedback messages, and recommendations improves the user experience and helps ensure that both applications provide coherent guidance.