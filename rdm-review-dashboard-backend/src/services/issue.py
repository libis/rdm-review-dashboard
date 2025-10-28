from typing import Optional, List
import shelve
import os
from persistence import filesystem
from services.dataverse.dataset import metadata
from services.dataverse import user
from utils.logging import logging
from models.note import IssueList, IssueDict
from datetime import datetime
from pathlib import Path
import json 
from datetime import datetime

from autochecks import autochecks
from autochecks.check import Check
from autochecks.check_result import CheckResult

ISSUE_DEFINITIONS_FILE: str|None = None
FEEDBACK_EMAIL:str = ""


def read_issue_definitions():
    result = None
    if ISSUE_DEFINITIONS_FILE is None:
        raise FileNotFoundError("Issue definitions file not set!")
    try:
        with open(Path(ISSUE_DEFINITIONS_FILE).absolute()) as f:
            result = json.load(f)
    except:
        logging.error(f"Could not read issue definitions from {ISSUE_DEFINITIONS_FILE}")
        raise
    return result


def get_last_autocheck_timestamp(persistent_id: str):
    return datetime.now()

def save_autocheck_results(persistent_id: str, check_results: dict[str, CheckResult]): 
    foldername = filesystem.get_foldername_from_persistent_id(persistent_id)
    file_path = [foldername, 'issues']
    base_dir = filesystem.BASE_DIR.copy()
    
    for folder in file_path:
        if not folder in os.listdir(os.path.join(*base_dir)):
            logging.info(f'adding {folder} to {os.listdir(os.path.join(*base_dir))}')
            os.mkdir(os.path.join(*base_dir, folder))
        base_dir.append(folder)
    results_file = shelve.open(os.path.join(*base_dir, 'autocheck_results'))
    try:
        results_file.update(check_results)
        result = True
    except Exception as e:
        logging.error(f"Error writing check results to file : {e}")
        result = False
    finally:
        results_file.close()
    return result
    
def load_autocheck_results(persistent_id: str) -> dict[str, CheckResult]|None:
    foldername = filesystem.get_foldername_from_persistent_id(persistent_id)
    base_dir = filesystem.BASE_DIR.copy()
    file_path = os.path.join(*base_dir, foldername, 'issues', 'autocheck_results')
    results_shelve = None
    result = None
    if not os.path.exists(file_path):
        return None
    try:
        results_shelve = shelve.open(file_path)
        result = dict(results_shelve)
    except Exception as e:
        logging.error(file_path + ": " + str(e))
    finally:
        if isinstance(results_shelve, shelve.Shelf):
            results_shelve.close()
    return result

def get_issue_categories(issue_definitions):
    categories = {}
    for k, v in issue_definitions.items():
        category = v['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(v['id'])
    result = []
    for k, v in categories.items():
        result.append({
            'id': k, 
            'label': k.title(),
            'issues': v 
        })
    return result

def get_available_autochecks():
    return autochecks.get_check_list()

def get_num_checks():
    checks = get_available_autochecks()
    if not isinstance(checks, list):
        return 0
    else:
        return len(checks)

async def get_details(persistent_id: str):
    '''Returns a dictionary containing manual checklist previously saved (if exists), automatically generated checklist, main categories of issues, and detailed descriptions of the issues.'''
    
    issue_definitions = read_issue_definitions()
    issues = get(persistent_id)
    issue_checklist_in_new_format = issues_to_new_format(issues.__dict__)
    autocheck_results : dict[str, CheckResult] = load_autocheck_results(persistent_id) or {}
    autocheck_states = {}
    autocheck_messages = {}
    autocheck_definitions = {}
    autocheck_timestamp = None
    for name, result in autocheck_results.items():
        if result.last_checked  and (not autocheck_timestamp or result.last_checked > autocheck_timestamp):
            autocheck_timestamp = result.last_checked
        autocheck_states[name] = result.result
        autocheck_messages[name] = result.warning
        autocheck_definitions[name] = result.definition
        
    result = {
        'details': [i for i in issue_definitions.values()],
        'auto': [],
        'manual_checklist': issue_checklist_in_new_format, 
        'auto_checklist_states': autocheck_states,
        'auto_checklist_messages': autocheck_messages,
        "autocheck_performed": autocheck_timestamp,
        'autochecks_available': get_num_checks(),
        'autocheck_definitions': autocheck_definitions,
        'categories': get_issue_categories(issue_definitions)
    }
    return result

def issues_to_new_format(issues: IssueDict)->dict:
    if not isinstance(issues, dict):
        return get_empty_issue_checklist()
    if isinstance(issues.get("issues"), list):
        return {k: True if k in issues.get("issues") else None for k in read_issue_definitions().keys()}
    elif isinstance(issues.get("issues"), dict):
        return issues.get("issues", {})

def get_empty_issue_checklist():
    ISSUE_DEFINITIONS = read_issue_definitions()
    return {k: None for k in ISSUE_DEFINITIONS.keys()}
        
        
def update_from_autochecks(persistent_id):
    issues = get(persistent_id)
    try:
        autocheck_results = autochecks.run_checks(persistent_id)
    except Exception as e:
        logging.error(f"Autochecks could not complete for {persistent_id} : {e}")
        raise e
    if not autocheck_results:
        raise Exception(f"Could not run autochecks for {persistent_id}")
    save_autocheck_results(persistent_id, autocheck_results)
    for name, check_result in autocheck_results.items():
        if check_result.result is not None:
            issues.issues[name] = check_result.result
    set(issues)
    
def get_autochecks(persistent_id):
    issues = get(persistent_id)
    try:
        autocheck_results = autochecks.run_checks(persistent_id)
    except Exception as e:
        logging.error(f"Autochecks could not complete for {persistent_id} : {e}")
        raise e
    if not autocheck_results:
        raise Exception(f"Could not run autochecks for {persistent_id}")
    save_autocheck_results(persistent_id, autocheck_results)
    set(issues)
    return issues

def set(issue_dict: IssueDict, user_id: Optional[str]=None):
    '''Updates the checklist for the dataset issues. If persistent_id/issues does not exist in fs, creates the folder/file. 
        Returns True if successful.'''
    # logging.info(f"Writing issues: {issue_dict.__dict__}")
    if not issue_dict.persistent_id:
        logging.error(f"Error writing issues to file : No dataset id.")
        return False
    foldername = filesystem.get_foldername_from_persistent_id(issue_dict.persistent_id)
    file_path = [foldername, 'issues']
    base_dir = filesystem.BASE_DIR.copy()
    for folder in file_path:
        if not folder in os.listdir(os.path.join(*base_dir)):
            logging.info(f'adding {folder} to {os.listdir(os.path.join(*base_dir))}')
            os.mkdir(os.path.join(*base_dir, folder))
        base_dir.append(folder)
    issues_file = shelve.open(os.path.join(*base_dir, 'checklist_state'))
    try:
        issues_file.update(issue_dict.__dict__)
        result = True
    except Exception as e:
        logging.error(f"Error writing issues to file : {e}")
        result = False
    finally:
        issues_file.close()
    return result

def get(persistent_id: str)->IssueDict:
    '''Reads the previously saved checklist for the dataset issues. Returns None if not found.'''
    file_path = os.path.join(*filesystem.BASE_DIR, filesystem.get_foldername_from_persistent_id(persistent_id), 'issues', 'checklist_state')
    issues = None
    try:
        issues = shelve.open(file_path)
        result = IssueDict(persistent_id=persistent_id, issues=issues.get("issues"))
    except Exception as e:
        logging.error(file_path + ": " + str(e))
        result = IssueDict(persistent_id=persistent_id, issues=get_empty_issue_checklist())
    finally:
        if isinstance(issues, shelve.Shelf):
            issues.close()
    if not result or result == {}:
        result = IssueDict(persistent_id=persistent_id, issues=get_empty_issue_checklist())
    return result


async def generate_feedback_email(persistent_identifier):
    """Generates a feedback email for the dataset contributor, based on previously saved issues checklist. The template in emails/feedback.txt and issue definitions in dataset_issue_definitions.json are used."""
    dataset_details = await metadata.async_get_dataset_details(persistent_identifier) 
    if not dataset_details or not isinstance(dataset_details, dict):
        raise Exception("Could not get dataset details")
    author_names = ', '.join([author_name.split(',')[-1].strip() for author_name in dataset_details.get('authorName', [])])
    try:
        reviewer_username = dataset_details.get('reviewer')[0]
        reviewer_info = await user.get_user_info(reviewer_username)
    except Exception as e:
        logging.error(e)
        reviewer_info = {}
    reviewer_name = reviewer_info.get('userfirstname', '')
    issue_details = await get_details(persistent_identifier)
    excluded_issues = [k for k, v in issue_details.get('manual_checklist', {}).items() if v==True]
    issue_definitions = [issue.get('message') for issue in issue_details.get('details') if issue.get('id') not in excluded_issues]
    issues_list = "\n".join([f"{num+1}. {issue}\n" for num, issue in enumerate(issue_definitions)])
    dataset_title = dataset_details.get('title')
    message = FEEDBACK_EMAIL 
    for k, v in {"{author_names}": author_names, "{dataset_title}":dataset_title, "{issues_list}":issues_list, "{reviewer_name}":reviewer_name}.items():
        message = message.replace(k, v)
    return message