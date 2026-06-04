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
from autochecks.autochecks import get_check_list
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



class PersistenceMode(Enum):
    REDIS = "REDIS"
    FS = "FS"


persistence_mode = None
check_modules = {}


def _initialize_consumer_config():
    import sys
    import autochecks.autochecks
    
    SETTINGS_FILE = os.environ.get("BACKEND_CONFIG_FILE") or "./config/backend_config.json"
    
    if not os.path.isabs(SETTINGS_FILE):
        script_dir = Path(__file__).parent 
        src_dir = script_dir.parent 
        
        resolved_path = (src_dir / SETTINGS_FILE).resolve()
        
        if not resolved_path.exists():
            resolved_path = (Path(os.getcwd()) / SETTINGS_FILE).resolve()
        
        SETTINGS_FILE = str(resolved_path)
    
    try:
        with open(SETTINGS_FILE) as f:
            settings = json.load(f)
        
        filesystem.BASE_DIR = [settings.get("dataPath")]
        utils.logging.configure_logging()
        native.BASE_URL = settings.get("DataverseAPI", "") + "/api"
        native.KEY_FILE = settings.get("DataverseAPIKeyFile", "")
        issue.DATAVERSE_URL = settings.get("DataverseURL", "")
        autochecks.autochecks.path = settings.get("automationsPath")
        if autochecks.autochecks.path and autochecks.autochecks.path + "/scripts" not in sys.path:
            sys.path.insert(1, autochecks.autochecks.path + "/scripts")
        autochecks.autochecks.default_timeout = settings.get("automationDefaultCheckTimeout")
        
        logging.info(f"Huey consumer initialized with config from {SETTINGS_FILE}")
        logging.info(f"Dataverse API: {native.BASE_URL}")
        logging.info(f"Data path: {filesystem.BASE_DIR}")
        logging.info(f"Automations path: {autochecks.autochecks.path}")
        
    except Exception as e:
        logging.error(f"Failed to initialize Huey consumer configuration: {e}")
        raise


_initialize_consumer_config()


redis_host = "cache"
redis_port = 6379
redis_db = 0
redis_pw = None
redis_max_connections = 20


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting"
    DONE = "done"
    FAILED = "failed"
    

#TODO: put switch case

pool = ConnectionPool(host=redis_host, port=redis_port, db=redis_db, max_connections=redis_max_connections)

huey = RedisHuey(
    name='rdb_autocheck',  
    connection_pool=pool,  
    immediate=False  
)
    
def import_module(check_name: str):
    module = None
    try:
        module = importlib.import_module(check_name)
    except Exception as e:
        logging.error(f"Could not import '{check_name}'. Check will be skipped.")
        return None
    
    try:
        _ = getattr(module, "run")
    except Exception as e:
        logging.error(f"Could not retrieve function 'run' in module '{check_name}': {e}")
        return None
    return module

def import_modules():
    result = {} 
    checks = get_check_list()
    for check in checks:
        check_name = check.name
        try:
            result[check_name] = import_module(check_name)
        except Exception as e:
            logging.error(f"Could not import '{check_name}'. Check will be skipped.")
            continue
    return result    

if not check_modules:  
    check_modules = import_modules()
    logging.info(f"Huey consumer: Loaded {len(check_modules)} check modules: {list(check_modules.keys())}")
