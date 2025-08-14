from autochecks.check import CheckResult, DatasetContext
from datetime import datetime


def run(context: DatasetContext) -> CheckResult:
    result: bool|None = None
    message: str|None = None
    return CheckResult(result, message, datetime.now())
