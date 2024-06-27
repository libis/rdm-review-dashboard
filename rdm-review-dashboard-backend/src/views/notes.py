import fastapi
from typing import Optional, List, Literal
from services import note
from models.note import NoteEntry, Taglist
from utils.generic import async_id_from_args, get_persistent_id
from utils import response_headers

router = fastapi.APIRouter()


@router.get("/api/datasets/{persistent_identifier:path}/notes")
@response_headers.inject_uid
async def get_notes_by_dataset_id(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    note_type: Optional[Literal["note", "history", "feedback", "review_tags"]] = None,
    tags: Optional[List[str]] = None,
):
    """Retrieves all notes of a type for the dataset with the persistent identifier."""
    note_type = note_type or "note"
    _notes = note.get_notes_by_dataset(persistent_identifier, note_type)
    return _notes


@router.get("/api/datasets/{persistent_identifier:path}/notes/{note_id}")
@response_headers.inject_uid
async def get_notes_by_note_id(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    note_id: str,
):
    """Retrieves a note with the given id for the dataset with the persistent identifier."""
    _note = note.get_note_by_id(persistent_identifier, note_id, "note")
    return _note


@router.post("/api/datasets/{persistent_identifier:path}/notes/{note_id}")
@response_headers.inject_uid
async def post_note_by_note_id(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    note_id: str,
    note_entry: NoteEntry,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Inserts a note with the given id to the dataset with the persistent identifier."""
    note_type = note_entry.note_type or "note"
    return note.upsert_note(
        persistent_identifier,
        note_entry.text,
        AJP_USER,
        note_type,
        note_id,
        note_entry.version,
        note_entry.tags,
    )


@router.post("/api/datasets/{persistent_identifier:path}/notes")
@response_headers.inject_uid
async def post_note(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    note_entry: NoteEntry,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Inserts the given note for the dataset with the persistent identifier, or updates it if the note with the id already exists."""
    note_type = note_entry.note_type or "note"
    note_id = None
    return note.upsert_note(
        persistent_identifier,
        note_entry.text,
        AJP_USER,
        note_type,
        note_id,
        note_entry.version,
        note_entry.tags,
    )


@router.get("/api/datasets/{persistent_identifier:path}/internal_note")
@response_headers.inject_uid
async def get_internal_note(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    """Inserts or updates the internal note for reviewers, for the dataset with the persistent identifier."""
    note_id = await async_id_from_args(persistent_identifier)
    _note = note.get_note_by_id(persistent_identifier, note_id, "note")
    return _note


@router.post("/api/datasets/{persistent_identifier:path}/internal_note")
@response_headers.inject_uid
async def replace_internal_note(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    note_entry: NoteEntry,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """ "Returns the internal note for reviewers, for the dataset with the persistent id."""
    note_id = await async_id_from_args(persistent_identifier)
    return note.upsert_note(
        persistent_identifier,
        note_entry.text,
        AJP_USER,
        "note",
        note_id,
        note_entry.version,
        note_entry.tags,
    )


@router.get("/api/datasets/{persistent_identifier:path}/history")
@response_headers.inject_uid
async def get_history(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    """Returns all the history items for the dataset with the persistent identifier."""
    _notes = note.get_notes_by_dataset(
        persistent_id=persistent_identifier, note_type="history"
    )
    return _notes


@router.get("/api/datasets/{persistent_identifier:path}/review_tags")
@response_headers.inject_uid
async def get_review_tags(
    response: fastapi.Response, request: fastapi.Request, persistent_identifier: str
):
    """Returns all the review tags for the dataset with the persistent identifier."""
    note_id = await async_id_from_args(persistent_identifier)
    _note = note.get_note_by_id(persistent_identifier, note_id, "review_tags")

    result = []
    if _note:
        result = _note.get("tags", [])

    return result


@router.post("/api/datasets/{persistent_identifier:path}/review_tags")
@response_headers.inject_uid
async def update_tags(
    response: fastapi.Response,
    request: fastapi.Request,
    persistent_identifier: str,
    tags: Taglist,
    AJP_USER: Optional[str] = fastapi.Header(default=None, convert_underscores=False),
):
    """Updates the review tags for the dataset with the persistent identifier."""
    note_id = await async_id_from_args(persistent_identifier)

    return note.upsert_note(
        persistent_identifier, "", "review_tags", AJP_USER, note_id, None, tags.tags
    )
