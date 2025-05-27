from autochecks.check import CheckResult, DatasetContext  # type: ignore
from datetime import datetime


def run(context: DatasetContext) -> CheckResult:
    result: bool|None = None
    message: str|None = None
    return CheckResult(result, message, datetime.now())
