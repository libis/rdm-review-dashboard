from datetime import datetime
from typing import List, Optional, Literal, Any
from pydantic import BaseModel
from autochecks.check_result import CheckResult
from autochecks.dataset_context import DatasetContext        

class Check(BaseModel): 
    name: str
    timeout: Optional[int|None] = None
    helpText: str