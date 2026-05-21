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
from autochecks.autochecks import get_check_list, get_module_name
from huey import RedisHuey, FileHuey
from enum import Enum
from datetime import datetime
from redis import ConnectionPool
from uuid import uuid4
import json 
from persistence import filesystem
import os
from services import issue
from services.dataverse import native
from pathlib import Path
import utils.logging
from autochecks.autocheck_cfg import huey, TaskStatus, check_modules


@huey.task()
def run_check_as_task(check_name: str, dataset_context: DatasetContext):
    persistent_id = dataset_context.persistent_id
    file_path = get_dataset_tasks_filepath(persistent_id) + [str(check_name)]
    
    # existing_state = read_state(file_path)
    # if existing_state and existing_state.get("status") == TaskStatus.DONE.value:
    #     logging.info(f"Task {check_name} for {persistent_id} already completed, skipping")
    #     return None
    
    check_module = check_modules.get(check_name)
    if not check_module:
        logging.error(f"Autocheck module {check_name} not loaded. ")
    state = {"id": persistent_id + "__" + check_name, 
             "task_id": f"{check_name}",
             "started": str(datetime.now()),
             "finished": None,
             "subtasks": None, 
             "results" : None,
             "status": TaskStatus.RUNNING.value
             }
    write_state(file_path, state)
    result = check_module.run(dataset_context)
    state["results"] = result.__dict__
    state["status"] = TaskStatus.DONE.value
    state["finished"] = str(datetime.now())
    write_state(file_path, state)
    return result

@huey.task()
def init_dataset_context_wrapper(persistent_id) -> DatasetContext:
    logging.info(persistent_id)
    return DatasetContext(persistent_id)

def write_state(file_path, state):
    filesystem.make_dir_if_not_exists(file_path[:-1])
    file_path = filesystem.BASE_DIR + file_path
    with open(f"{os.path.join(*file_path)}.json", "w") as f:
        json.dump(state, f)

def read_state(file_path):
    file_path = filesystem.BASE_DIR + file_path
    try:
        with open(f"{os.path.join(*file_path)}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_dataset_tasks_filepath(dataset_id):
    return [filesystem.get_foldername_from_persistent_id(dataset_id), "tasks"]


