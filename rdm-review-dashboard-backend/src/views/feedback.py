import fastapi
from typing import Optional
from services import note, issue
from models.note import NoteEntry
from utils.generic import async_id_from_args
from utils import response_headers
from utils.logging import logging

router = fastapi.APIRouter()


@router.get("/api/datasets/{persistent_identifier:path}/feedback/:generate")
@response_headers.inject_uid
async def generate_feedback(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Returns a feedback email, autogenerated using the issues checklist. Configuration in dataset_issue_definitions.json and emails/feedback.txt"""
    note_id = await async_id_from_args(persistent_identifier)
    try:
        feedback_text = await issue.generate_feedback_email(persistent_identifier)
    except Exception as e:
        logging.error(e)
        raise fastapi.HTTPException(status_code=404, detail="Dataset not found")
    note.upsert_note(
        persistent_identifier, feedback_text, AJP_USER, "feedback", note_id
    )
    _note = note.get_note_by_id(persistent_identifier, note_id, "feedback")
    return _note


@router.get("/api/datasets/{persistent_identifier:path}/feedback")
@response_headers.inject_uid
async def get_feedback(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Returns the previously saved feedback email."""
    note_id = await async_id_from_args(persistent_identifier)
    _note = note.get_note_by_id(persistent_identifier, note_id, "feedback")
    if not _note:
        try:
            feedback_text = await issue.generate_feedback_email(persistent_identifier)
            note.upsert_note(
                persistent_identifier, feedback_text, AJP_USER, "feedback", note_id
            )
            _note = note.get_note_by_id(persistent_identifier, note_id, "feedback")
        except Exception as e:
            logging.error(e)
            raise fastapi.HTTPException(status_code=404, detail="Dataset not found")
    return _note


@router.post("/api/datasets/{persistent_identifier:path}/feedback")
@response_headers.inject_uid
async def replace_feedback(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    note_entry: NoteEntry,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Saves the feedback email."""
    note_id = await async_id_from_args(persistent_identifier)
    return note.upsert_note(
        persistent_identifier, note_entry.text, AJP_USER, "feedback", note_id
    )
