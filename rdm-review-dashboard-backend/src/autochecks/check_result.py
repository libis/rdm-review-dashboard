from pydantic import BaseModel
from datetime import datetime
from typing import List

class CheckResult(BaseModel): 
    check_result: bool | None = None
    last_checked: datetime | None = None
    message: str | None = None
    
    def __init__(self, check_result:bool|None, message:str|None, check_datetime=None):
        super().__init__()
        
        self.check_result = check_result
        self.last_checked = check_datetime or datetime.now()
        self.message = message
        if self.check_result == True and self.message is not None:
            raise ValueError("Message must be empty when check_result is True.") 
