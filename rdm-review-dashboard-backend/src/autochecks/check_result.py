from pydantic import BaseModel 
from datetime import datetime
from typing import List

class CheckResult(BaseModel): 
    result: bool | None = None
    last_checked: datetime | None = None
    warning: str | None = None
    
    def __init__(self, check_result:bool|None, warning:str|None, check_datetime=None):
        super().__init__()
        
        self.result = check_result
        self.last_checked = check_datetime or datetime.now()
        self.warning = warning
        if self.result == True and self.warning is not None:
            raise ValueError("Warning must be empty when check_result is True.")