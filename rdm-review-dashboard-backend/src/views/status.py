import fastapi
from typing import Literal, Optional
from services import email
from services.dataverse.dataset import metadata
from utils.logging import logging
from utils import response_headers
from services import history

router = fastapi.APIRouter()


@router.post("/api/datasets/{persistent_identifier:path}/status")
@response_headers.inject_uid
async def set_status(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    to_status: str,
    version: Optional[Literal["minor", "major", "updatecurrent"]] = None,
    reason: Optional[str] = None,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    res = await metadata.change_status(
        persistent_identifier, to_status, version, reason, Ajp_uid
    )
    if res.status_code == 200:

        history_update = f"Dataset status changed to {to_status}."
        subcategory = f"{to_status}"
        tags = [
            {"type": "category", "content": "Status Change"},
            {"type": "subcategory", "content": f"{subcategory}"},
        ]

        history.append_to_history(
            persistent_identifier, history_update, user_id=Ajp_uid
        )
    return res.text


@router.post("/api/datasets/{persistent_identifier:path}/:publish")
@response_headers.inject_uid
async def publish_dataset(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    version: Literal["minor", "major", "updateCurrent"] = None,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    res = await metadata.change_status(
        persistent_identifier, "published", version, Ajp_uid
    )
    if res.status_code == 200:
        if version == "updateCurrent":
            version_text = "without version change"
        else:
            version_text = f"as a {version} version"
        history_update = f"Dataset published by {Ajp_uid} {version_text}."
        tags = [
            {"type": "category", "content": "Status Change"},
            {"type": "subcategory", "content": "Published"},
        ]
        history.append_to_history(
            persistent_identifier, history_update, user_id=Ajp_uid, tags=tags
        )
    return res.text


@router.post("/api/datasets/{persistent_identifier:path}/:return")
@response_headers.inject_uid
async def return_dataset(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    reason: Optional[str] = None,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    res = await metadata.change_status(persistent_identifier, "draft", reason, Ajp_uid)
    if res.status_code == 200:
        history_update = f"Dataset returned to author by {Ajp_uid}."
        tags = [
            {"type": "category", "content": "Status"},
            {"type": "subcategory", "content": "Returned to Author"},
        ]

        history.append_to_history(
            persistent_identifier, history_update, user_id=Ajp_uid, tags=tags
        )
        await email.send_feedback_email(persistent_identifier, Ajp_uid)
        logging.info(f"Dataset {persistent_identifier} returned to author.")
    else:
        logging.error(
            f"Dataset {persistent_identifier} could not be returned to author. {res.status_code, res.text}"
        )

    return res.text


@router.post("/api/datasets/{persistent_identifier:path}/:deaccession")
@response_headers.inject_uid
async def deaccession_dataset(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    res = await metadata.change_status(persistent_identifier, "deaccessioned", Ajp_uid)
    if res.status_code == 200:
        history_update = f"Dataset deaccessioned by {Ajp_uid}."
        tags = [
            {"type": "category", "content": "Status"},
            {"type": "subcategory", "content": "Deaccesioned"},
        ]

        history.append_to_history(
            persistent_identifier, history_update, user_id=Ajp_uid, tags=tags
        )
        logging.info(f"Dataset {persistent_identifier} deaccessioned.")
    else:
        logging.error(
            f"Dataset {persistent_identifier} could not be deaccessioned. {res.status_code, res.text}"
        )
    return res.text


@router.post("/api/datasets/{persistent_identifier:path}/:submit")
@response_headers.inject_uid
async def submit_for_review_dataset(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    res = await metadata.change_status(persistent_identifier, "in_review", Ajp_uid)
    if res.status_code == 200:
        history_update = f"Dataset submitted for review {Ajp_uid}."
        tags = [
            {"type": "category", "content": "Status"},
            {"type": "subcategory", "content": "Submited for Review"},
        ]

        history.append_to_history(
            persistent_identifier, history_update, user_id=Ajp_uid, tags=tags
        )
        logging.info(f"Dataset {persistent_identifier} submitted for review.")
    else:
        logging.error(
            f"Dataset {persistent_identifier} could not be submitted for review. {res.status_code, res.text}"
        )
    return res.text


@router.get("/api/datasets/{persistent_identifier:path}/status")
@response_headers.inject_uid
async def get_dataset_status(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    result = await metadata.get_dataset_status(persistent_identifier)
    return result
