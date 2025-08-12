from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from autochecks.check import Check

class IssueList(BaseModel):
    persistent_id: Optional[str] = None
    issues: List[str] = []

class IssueDict(BaseModel):
    persistent_id: Optional[str] = None
    issues: dict[str, bool|None] = {}
    
class Tag(BaseModel):
    tag_id: Optional[str] = None
    type: Optional[str] = None
    content: str

class Taglist(BaseModel):
    tags: Optional[List[Tag]] = []

class Note(BaseModel):
    text: Optional[str]
    created: Optional[datetime] 
    modified: Optional[datetime]
    persistentId: Optional[str]
    version: Optional[str]
    userId: Optional[str]
    noteId: str
    tags: Optional[List[Tag]]
    noteType: str
class NoteEntry(BaseModel):
    text: Optional[str]
    version: Optional[str] = None
    tags: Optional[List[Tag]] = []
    note_type: Optional[str] = None
