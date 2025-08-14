from pydantic import BaseModel
from datetime import datetime
from typing import List

class CheckResult(BaseModel): 
    check_result: bool|None = None
    last_checked: datetime | None = None
    message: str | None = None
    checked: bool = False
    duration: float|None = None
    
    def __init__(self, check_result:bool|None, message:str|None, check_datetime=None):
        super().__init__()
        self.check_result = check_result
        self.last_checked = check_datetime or datetime.now()
        self.message = message

