
from autochecks.check_result import CheckResult
from autochecks.dataset_context import DatasetContext
from typing import List, Optional
from utils.logging import logging
import importlib
import asyncio

check_list = []

    
def run_checks(persistent_id: str) -> List[CheckResult]:
    logging.info(f"Running autochecks on {persistent_id}")
    context = DatasetContext(persistent_id)


    result = []
    for check in check_list:
        logging.info(f"Running autocheck {check} on {persistent_id}")
        module = importlib.import_module("autochecks." + check)
        method = getattr(module, "run")        
        if not asyncio.iscoroutinefunction(method):
            check_result : CheckResult = method(context)
            logging.info("{check} on {persistent_id} result: {check_result.check_result}, message: {check_result.message}")
            result.append(check_result)
    return result
        
        
    
