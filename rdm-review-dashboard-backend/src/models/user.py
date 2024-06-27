from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class UserRole(Enum):
    ADMIN = 1
    REVIEWER = 9
    CURATOR = 7
    _UNUSED_CONTRIBUTOR = 5
    CONTRIBUTOR = 6


class User(BaseModel):
    user_id: str
    role: int
    faculties: Optional[List[str]]
    departments: Optional[List[str]]


