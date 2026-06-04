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
from autochecks.autocheck_tasks import run_check_as_task
    
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

def orchestrate_autochecks(dataset_id):
    logging.info("Orchestrating autochecks for dataset: " + dataset_id)
    
    orchestrator_task_file_path = get_dataset_tasks_filepath(dataset_id) + ["orchestrator"]
    # existing_orchestrator = read_state(orchestrator_task_file_path)
    # if existing_orchestrator:
    #     existing_status = existing_orchestrator.get("status")
    #     if existing_status == TaskStatus.RUNNING.value:
    #         logging.info(f"Orchestration already in progress for {dataset_id}, using existing task IDs")
    #         # Return existing subtask IDs if they exist
    #         return existing_orchestrator
    #     elif existing_status == TaskStatus.DONE.value:
    #         logging.info(f"Orchestration already completed for {dataset_id}")
    #         return existing_orchestrator
    branches  = []
    subtask_ids = list(check_modules.keys())
    state = {"id": dataset_id, 
             "task_id": "autocheck_orchestrator",
             "started": str(datetime.now()),
             "finished": None,
             "subtasks": subtask_ids, 
             "results" : None,
             "status": TaskStatus.RUNNING.value
             }
    write_state(orchestrator_task_file_path, state)
    dataset_context = DatasetContext(dataset_id)
    for check_id, check_module in check_modules.items():
        logging.info(f"Queueing check task: {check_id}")
        # Pass only serializable data (strings) to the task
        j = run_check_as_task(check_id, dataset_context)
        branches.append(j)
        subtask_ids.append(j.id)
    return state

def get_check_status(persistent_id):
    file_path = get_dataset_tasks_filepath(persistent_id) + ["orchestrator"]
    task_state = read_state(file_path) 
    subtask_statuses = {}
    if task_state is None:
        return None
    for subtask in task_state.get("subtasks", []):
        subtask_path = get_dataset_tasks_filepath(persistent_id) + [subtask]
        subtask_state = read_state(subtask_path) or {}
        subtask_statuses[subtask] = subtask_state
    issue_definitions = issue.read_check_my_dataset_issue_definitions()
    issue_categories = issue.get_issue_categories(issue_definitions)
    issue_details = []
    for k, v in issue_definitions.items():
        current_issue = {}
        current_issue.update(v)
        current_issue["id"] = k
        issue_details.append(current_issue)
        
    return {
        "tasks": list(subtask_statuses.values()),
        "structure": issue_categories,
        "details": issue_details
        }

