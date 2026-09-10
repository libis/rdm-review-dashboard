# Review workflow

## Overview

The review dashboard supports the review of datasets submitted through Dataverse.

The review workflow consists of 4 main steps

Selection -> Details -> Feedback -> Publish / Return

Datasets move through these stages as reviewers assess the dataset, provide feedback and decide whether it is ready for publication.


## Starting a review

1. Log in 
2. Open the **Submitted for Review** tab.
3. Select the dataset you want to review.
4. Click **Assign** to assign the dataset to yourself.
5. Open the review using **View details**

Administrators can additionally assign reviews to other reviewers and take over reviews when necessary.


## Reviewing the dataset

### Inspect the dataset

The **Details** screen provides access to:

- Dataset metadata: DOI, Title, Author, current version
- Dataset size information
- A direct link to the dataset landing page in Dataverse
- Buttons to **Contact the dataset creator(s)**, **Ask for support** or **View History**
- A checklist with all items to review

Reviewers should inspect the dataset and verify that it meets the requirements of their repository before publication.

### Complete the Review checklist

The review checklist contains the requirements that must be evaluated before publication.

Checklist items are grouped into categories and may be:

- manually reviewed;
- supported by automated checks.

To enable the autochecks, click on the *Run Autochecks* button. All parameters that are automatically checked will be grayed out. The other parameters (the ones remaining with a white background) have not been checked. 

The autocheck result is displayed:

   - ✅ success: The parameters have been correctly filled in the dataset.
   - ❌ failure: The checklist item is not satisfied.
   - ⚠️ warning: The parameters that have not been correctly filled and require more attention. Upon hovering on the warning sign, a small pop-up text will give you more information on the possible issues.

You can apply autochecks by clicking on the *Apply all autochecks* button. This should be done only after a manual check of all parameters. 

Autochecks can help identify potential issues in metadata or dataset files, but reviewers remain responsible for making the final review decision.

### Add internal notes

The **Internal Notes** section can be used to record observations during the review.

The internal notes are not shared with the dataset creators, but are shared with the helpdesk when **ask for support** is clicked. They also persist between reviewers and reviews.

### Request support

If additional support is required:

1. Record relevant information in the **Internal Notes** section.
2. Select **Ask for support**.

This action adds a support flag to the dataset and notifies the configured support contacts. 


## Generate and review feedback

After completing the checklist, proceed to the **Feedback** screen. 

### Summary

The summary contains:

- Unresolved issues
- Review notes

Issues displayed in the summary correspond to checklist items that have not been marked as completed.

### Feedback

A feedback email is automatically generated using:

- the completed review checklist;
- issue definitions;
- the configured feedback email template.

The generated feedback can be reviewed and edited before it is sent.

Reviewers are encouraged to add additional guidance where helpful.

If checklist items are modified after feedback has already been generated, the reviewer must select *Generate from Checklist* to regenerate the feedback email. This action replaces the previously generated version.


## Finalise the review

The final step is deciding whether the dataset is ready for publication.

### Publish the dataset

If the dataset satisfies the repository's review requirements:

1. Select **Publish**
2. Choose the appropriate release type
3. Confirm publication

Depending on the dataset version, one of the following release options may be available:

- **Major** release: increases the major version of the dataset, such as 1.0 to 2.0.
- **Minor** release: increases the minor version, such as 1.0 to 1.1.
- **Update current version**

If the dataset is previously not released it will be released as 1.0.

### Return the dataset for revision

If issues remain:

1. Select **Return**
2. Review the generated feedback email
3. Confirm the return action

The contributor will receive the feedback email and can revise the dataset before resubmitting it for review.


## Responsibilities

Reviewers are responsible for:

- Reviewing submitted datasets
- Completing review checklists
- Evaluating autocheck results
- Recording review notes
- Generating / adapting feedback
- Deciding whether a dataset should be published or returned for revision

Administrators have all reviewer capabilities and may additionally:

- Assign reviews to other reviewers
- Reassign reviews
- Take over reviews when necessary
- Handle exceptional review situations