from datetime import datetime
from services import note
from typing import Optional, List
from utils.generic import id_from_args
from utils.logging import logging


def append_to_history(
    persistent_id: str,
    text: str,
    user_id: str,
    version: Optional[str] = None,
    tags: Optional[List[note.Tag]] = None,
):
    """Adds the given text, dataset version, list of tags, created & modified datetime to history."""
    now = datetime.now()
    note_type = "history"
    note_id = id_from_args(persistent_id, now, note_type)
    text = text or ""
    return note.upsert_note(persistent_id, text, user_id, "history", note_id, version, tags)


def add_feedback_to_history(
    persistent_id: str,
    user: str,
    author: str,
    version: Optional[str] = None,
    feedback: Optional[str] = None,
):
    """Adds feedback sent to author when returning to the author to the history."""
    history_update = f"Feedback sent to {author}: \n{feedback}"
    return append_to_history(
        persistent_id, history_update, user_id=user, version=version
    )
