from autochecks.check_result import CheckResult
from autochecks.check import Check
from autochecks.dataset_context import DatasetContext
from typing import List, Optional, Callable
from utils.logging import logging
import importlib
import asyncio
import time
from multiprocessing import Process, Queue
import time
import json
from typing import List, Optional
from pydantic import BaseModel
from autochecks.check import Check

path = None
default_timeout = None

def get_check_list() -> List[Check]:
    check_list: List[Check] = []
    if not path:
        return check_list
    with open(path + "/autochecks.json") as f:
        checks = json.loads(f.read())
        for check in checks:
            timeout = check.get("timeout")
            if  timeout is None:
                timeout = default_timeout

            check_list.append(
                Check(
                    name = check.get("name"),
                    timeout= timeout
                )
            )
    return check_list

def wrapper(func, context, q):
    try:
        result = func(context)
        q.put(result)
    except Exception as e:
        q.put(e)


def run_function(func: Callable, context: DatasetContext, timeout:int|None):
    if not timeout or timeout <= 0:
        return func(context)
    
    q = Queue()
    p = Process(target=wrapper, args=(func, context, q))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        raise Exception(f"{func.__name__} in {get_module_name(func)} for {context.persistent_id} timed out after {timeout} seconds.")
    return q.get()

def get_module_name(method: Callable):
    try:
        return method.__module__.split(".")[-1]
    except:
        raise Exception("Could not retrieve method name")
    

def perform_check(method: Callable, context:DatasetContext, timeout: int|None):
        check_result : CheckResult = CheckResult(None, None)
        try:
            check_result = run_function(method, context, timeout)
        except Exception as e:
            logging.error(e)
            logging.error(f"Check {get_module_name(method)} could not complete in {timeout} seconds. Skipping...")
        return check_result
  
def run_checks(persistent_id: str) -> dict[str, CheckResult]:
    logging.info(f"Running autochecks on {persistent_id}")
    result = dict()

    context : DatasetContext 
    try:
        context = DatasetContext(persistent_id)
    except Exception as e:
        logging.error(f"Error retrieving context for dataset {persistent_id}: {e}")
        return result

    checks = get_check_list()
    for check in checks:
        check_name = check.name
        
        try:
            module = importlib.import_module(check_name)
        except Exception as e:
            logging.error(f"Could not import '{check_name}'. Check will be skipped.")
            continue
        
        try:
            method = getattr(module, "run")
        except Exception as e:
            logging.error(f"Could not retrieve function 'run' in module '{check_name}': {e}")
            continue
        
        if asyncio.iscoroutinefunction(method):
            raise Exception("Coroutines not supported.")
        
        logging.info(f"Running autocheck {check_name} on {persistent_id}...")
        check_result = perform_check(method, context, check.timeout)
        if isinstance(check_result, Exception):
            logging.error(check_result)
            check_result = CheckResult(None, None)
        logging.info(f"{get_module_name(method)} on {context.persistent_id} result: {check_result.result}, warning message: {check_result.warning}")
        result[check_name] = check_result
        
    return result    