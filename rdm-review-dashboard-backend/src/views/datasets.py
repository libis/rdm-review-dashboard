import fastapi
from typing import Optional
from utils.logging import logging
from services.dataverse.dataset import metadata
from services import issue
from models.note import IssueList
from utils import response_headers

router = fastapi.APIRouter()


@router.get("/api/datasets")
@response_headers.inject_uid
async def async_get_datasets_details(
    response: fastapi.Response,
    request: fastapi.Request,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
    start: Optional[int] = fastapi.Query(default=None),
    rows: Optional[int] = fastapi.Query(default=None),
    status: Optional[str] = fastapi.Query(default=None),
    reviewer: Optional[str] = fastapi.Query(default=None),
):
    """Retrieves a list of all datasets, merged with their details."""
    datasets = await metadata.async_get_datasets_details(
        start, rows, status, reviewer=reviewer
    )
    return datasets


@router.post("/api/datasets/{persistent_identifier:path}/issues/checklist")
@response_headers.inject_uid
async def update_dataset_issues(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    issues: Optional[issue.IssueList] = None,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Saves a list of strings, representing issues to the specified dataset."""
    if not issues:
        issues = IssueList()
    issues.persistent_id = persistent_identifier
    issue.set(issues, AJP_USER)
    return issues


@router.get("/api/datasets/{persistent_identifier:path}/issues")
@response_headers.inject_uid
async def get_dataset_issues(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Retrieves the specified dataset's issues."""
    datasets = await issue.get_details(persistent_identifier)
    return datasets


@router.get("/api/datasets/{persistent_identifier:path}/contact")
@response_headers.inject_uid
async def get_dataset_contact(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Retrieves the specified dataset's contact."""
    contact = await metadata.get_dataset_contact(persistent_identifier)
    return contact


@router.get("/api/datasets/stats/reviewStatus")
@response_headers.inject_uid
async def async_get_datasets_details(
    response: fastapi.Response,
    request: fastapi.Request,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
    reviewer: Optional[str] = fastapi.Query(default=None),
):
    """Retrieves a list of all status counts for datasets."""
    datasets = await metadata.get_review_status_counts(reviewer=reviewer)
    return list(datasets.values())


@router.get("/api/datasets/{persistent_identifier:path}")
@response_headers.inject_uid
async def get_dataset_details(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Retrieves the specified dataset's details."""
    datasets = await metadata.async_get_dataset_details(persistent_identifier)
    return datasets
