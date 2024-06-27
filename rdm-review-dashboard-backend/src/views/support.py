import fastapi
from typing import Optional
from utils.logging import logging
from utils.generic import async_id_from_args
from services import email, note
from utils import response_headers
from services import history

router = fastapi.APIRouter()


async def get_tags(persistent_identifier, _type=None, text=None):
    """Returns all the tags that are set for a dataset, with optional filters for "type" and "text"(content)."""
    note_id = await async_id_from_args(persistent_identifier)
    _note = note.get_note_by_id(persistent_identifier, note_id, "review_tags")
    result = []
    for tag in _note.get("tags", []):
        if (_type and tag.get("type") != _type) or (
            text and tag.get("content") != text
        ):
            continue
        else:
            result.append(tag)
    return result


@router.get("/api/datasets/{persistent_identifier:path}/support_request")
@response_headers.inject_uid
async def get_support_request(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Returns the tags of  the type "support" of a dataset."""
    tags = await get_tags(persistent_identifier, _type="support")
    return tags


@router.post("/api/datasets/doi:{persistent_identifier:path}/support_request")
@response_headers.inject_uid
async def ask_support(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Adds the "Support requested" tag to a dataset and sends an email to the configured helpdesk email address."""
    note_id = await async_id_from_args(persistent_identifier)
    tag = {"type": "support", "content": "Support Requested"}
    success = note.upsert_note(
        persistent_identifier, "", Ajp_uid, "review_tags", note_id, None, [tag]
    )

    history_update = f"Support requested by {Ajp_uid}."
    tags = [
        {"type": "category", "content": "Support Request"},
        {"type": "subcategory", "content": "Requested"},
    ]

    history.append_to_history(
        persistent_identifier, history_update, user_id=Ajp_uid, tags=tags
    )

    email_result = await email.send_support_requested_email(
        persistent_identifier, Ajp_uid, remove=False
    )

    tags = await get_tags(persistent_identifier, _type="support")
    return tags


@router.delete("/api/datasets/doi:{persistent_identifier:path}/support_request")
@response_headers.inject_uid
async def remove_support_request(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    Ajp_uid: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Removes the "Support requested" tag from the dataset and sends an email to the configured helpdesk email address."""
    note_id = await async_id_from_args(persistent_identifier)
    success = note.upsert_note(
        persistent_identifier, "", Ajp_uid, "review_tags", note_id, None, []
    )

    history_update = f"Support request removed by {Ajp_uid}."
    tags = [
        {"type": "category", "content": "Support Request"},
        {"type": "subcategory", "content": "Request Removed"},
    ]
    history.append_to_history(
        persistent_identifier, history_update, user_id=Ajp_uid, tags=tags
    )

    email_result = await email.send_support_requested_email(
        persistent_identifier, Ajp_uid, remove=True
    )
    tags = await get_tags(persistent_identifier, _type="support")

    return tags
