import shelve
import os
from persistence import filesystem
from utils.logging import logging
from models.note import Note, Tag
from utils.generic import id_from_args
from time import sleep
from typing import List, Optional
from datetime import datetime


def upsert_note(    
    persistent_identifier: str,
    text: str,
    user_id: str,
    note_type: str,
    note_id: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[dict]] = None,
    ):
    """Inserts or updates a note saved in filesystem."""
    
    now = datetime.now()
    tags = tags or []

    for i, tag in enumerate(tags):
        tag['tag_id'] = tag.get('tag_id') or id_from_args(
            tag.get("content"), tag.get("type")
        )

    if not note_id:
        note_id = id_from_args(persistent_identifier, note_type, now)

    note = Note(
        userId=user_id,
        persistentId=persistent_identifier,
        version=version,
        noteId=note_id,
        text=text,
        tags=[Tag(**tag) for tag in tags], 
        noteType=note_type,
        created=None,
        modified=now,
    )

    dataset_foldername = filesystem.get_foldername_from_persistent_id(note.persistentId)
    # to be saved as persistent_id/note_type/note_id
    file_path = [dataset_foldername, note.noteType] 
    note_file = open_note([*file_path, note.noteId])
    try:
        if not note_file:
            note.created = note.modified
            logging.info(
                f"Creating new note in file {os.path.join(*file_path, note.noteId)}"
            )
        else:
            note.created = note_file.get("created")
            logging.info(f"Updating note in file {os.path.join(*file_path, note.noteId)}")
        note_file.update(note.dict())
    finally:
        if note_file:
            try:
                note_file.close()
            except Exception:
                pass


def get_note_by_id(persistent_id: str, note_id: str, note_type: str) -> dict:
    """Reads a note from the filesystem."""
    result = {}
    file_path = [filesystem.get_foldername_from_persistent_id(persistent_id), note_type, note_id]
    result = read_note(file_path)
    return result


def read_note(file_path=List[str], retries: int = 5, waittime_in_s: int = 5):
    """Opens the note in the path, with given number of retries. Raises exception if file not found"""
    result = {}
    note = open_note(file_path, retries, waittime_in_s)
    if note:
        result = dict(note)
        note.close()
    return result


def open_note(file_path=List[str], retries: int = 5, waittime_in_s: int = 5):
    """Opens the note in the path, with given number of retries. Creates a new note if file does not exist."""
    filesystem.make_dir_if_not_exists(file_path[:-1])
    file_path = filesystem.BASE_DIR + file_path
    while retries > 1:
        try:
            note = shelve.open(os.path.join(*file_path))
            return note
        except Exception as e:
            sleep(waittime_in_s)
            retries -= 1
    logging.error(f"Cannot read note: {os.path.join(*file_path)}")
    return False


def get_notes_by_dataset(persistent_id: str, note_type: str):
    """Gets all the notes of a given type for a dataset."""
    file_path = [filesystem.get_foldername_from_persistent_id(persistent_id), note_type]
    result = []
    try:
        dir_contents = os.listdir(os.path.join(*filesystem.BASE_DIR, *file_path))
    except:
        dir_contents = []
    for file in dir_contents:
        note = read_note([*file_path, file])
        result.append(note)
    return result
