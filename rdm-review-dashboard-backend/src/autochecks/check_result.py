from pydantic import BaseModel 
from datetime import datetime

class CheckResult(BaseModel): 
    definition: str = ""
    result: bool | None = None
    last_checked: datetime | None = None
    warning: str | None = None
    additional_info: dict | None = None

    def __init__(self, check_result:bool|None, warning:str|None, additional_info: dict|None=None, check_datetime=None):
        super().__init__()
        self.result = check_result
        self.last_checked = check_datetime or datetime.now()
        self.warning = warning 
        self.additional_info = additional_info or None 
        if self.result == True and self.warning is not None:
            raise ValueError("Warning must be empty when result is True.")