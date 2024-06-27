import fastapi
from services.dataverse import user
from typing import Optional
from services.dataverse.dataset import assignee
from utils.logging import logging
from utils import response_headers
from services import history

router = fastapi.APIRouter()


@router.post("/api/datasets/{persistent_identifier:path}/reviewer")
@response_headers.inject_uid
async def set_reviewer(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    reviewer: str,
):
    """Assigns a reviewer to a dataset."""
    res = None
    res = assignee.set_reviewer(persistent_identifier, reviewer.strip("@"))
    if res.status_code == 200:
        history_update = f"Reviewer assigned: {reviewer}."
        tags = [
            {"type": "category", "content": "Reviewer Change"},
            {"type": "subcategory", "content": "Assigned"},
        ]
        history.append_to_history(
            persistent_identifier,
            history_update,
            user_id=request.headers.get("Ajp_uid"),
            tags=tags,
        )
        logging.info(f"Reviewer assigned: {persistent_identifier} -> {reviewer}")

    else:

        logging.error(
            f"Could not assign reviewer: {persistent_identifier} -> {reviewer}"
        )
        if res:
            logging.error(f"{res.status_code}. {res.text}")

    return res.text


@router.post("/api/datasets/{persistent_identifier:path}/reviewer/:replace")
@response_headers.inject_uid
async def replace_reviewer(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    reviewer: str,
):
    """Replaces the reviewer of a dataset."""
    res = None
    res = assignee.delete_all_reviewers(persistent_identifier)
    res = assignee.set_reviewer(persistent_identifier, reviewer)
    tries = 5
    for i in range(tries):
        res_ = assignee.get_dataset_assignees(persistent_identifier)
    if res.status_code == 200:
        history_update = f"Reviewer changed to: {reviewer}."
        tags = [
            {"type": "category", "content": "Reviewer Change"},
            {"type": "subcategory", "content": "Assigned"},
        ]
        history.append_to_history(
            persistent_identifier,
            history_update,
            user_id=request.headers.get("Ajp_uid"),
            tags=tags,
        )
        logging.info(f"Reviewer assigned: {persistent_identifier} -> {reviewer}")

    else:
        logging.error(
            f"Could not assign reviewer: {persistent_identifier} -> {reviewer}"
        )
        if res:
            logging.error(f"{res.status_code}. {res.text}")

    return res.text


@router.delete("/api/datasets/{persistent_identifier:path}/reviewer")
@response_headers.inject_uid
async def delete_reviewer(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    reviewer: Optional[str] = None,
):
    """Deletes a reviewer(s) from a dataset."""
    res = None
    res = assignee.delete_reviewer(
        persistent_id=persistent_identifier, user_id=reviewer
    )
    if res and res.status_code == 200:
        history_update = f"Reviewer deleted."
        tags = [
            {"type": "category", "content": "Reviewer Change"},
            {"type": "subcategory", "content": "Deleted"},
        ]

        history.append_to_history(
            persistent_identifier,
            history_update,
            user_id=request.headers.get("Ajp_uid"),
            tags=tags,
        )
        logging.info(f"Reviewer deleted: {persistent_identifier} -> {reviewer}")

    else:
        logging.error(
            f"Could not delete reviewer: {persistent_identifier} -> {reviewer}"
        )
        if res:
            logging.error(f"{res.status_code}. {res.text}")
    return True


@router.get("/api/datasets/{persistent_identifier:path}/assignees/contributor")
@response_headers.inject_uid
async def get_dataset_contributor(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    """Retrieves contributor information for the dataset."""
    assignees = assignee.get_dataset_assignees(persistent_identifier)
    contributors = assignees.get("contributor", [])
    result = []
    for contributor in contributors:
        details = await user.get_user_info(contributor)
        result.append(details)
    return result


@router.get("/api/datasets/{persistent_identifier:path}/reviewer")
@response_headers.inject_uid
async def get_dataset_reviewers(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    assignees = assignee.get_dataset_assignees(persistent_identifier).get(
        "reviewer", []
    )
    return assignees


@router.get("/api/datasets/{persistent_identifier:path}/assignees")
@response_headers.inject_uid
async def get_dataset_assignees(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    assignees = assignee.get_dataset_assignees(persistent_identifier)
    return assignees


@router.get("/api/reviewers")
@response_headers.inject_uid
async def get_dataverse_reviewers(response: fastapi.Response, request: fastapi.Request):
    result = []
    users = await user.get_dataverse_assignees(["admin", "reviewer"])
    for _user in users:
        if _user.get("isAdmin", False) or _user.get("isReviewer", False):
            result.append(_user)
    return users


@router.get("/api/users/{user_id}")
@response_headers.inject_uid
async def get_user(response: fastapi.Response, request: fastapi.Request, user_id: str):
    if user_id in {"me", ":me"}:
        user_id = response.headers.get("X-User")
    logging.info(f"looking up user: {user_id}")
    result = {"id": user_id}
    user_id = user_id.strip("@")
    roles = await user.get_user_roles(user_id)
    result.update(roles)
    return result


@router.get("/api/users/")
@response_headers.inject_uid
async def get_dataverse_assignees(response: fastapi.Response, request: fastapi.Request):
    return await user.get_dataverse_assignees(["admin", "reviewer"])
