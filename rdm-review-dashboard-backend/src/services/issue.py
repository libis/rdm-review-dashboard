
from typing import Optional
import shelve
import os
from persistence import filesystem
from services.dataverse.dataset import metadata
from services.dataverse import user
from utils.logging import logging
from models.note import IssueList

ISSUE_DEFINITIONS = {}
FEEDBACK_EMAIL:str = ""

async def get_details(persistent_id: str):
    '''Returns a dictionary containing manual checklist previously saved (if exists), automatically generated checklist, main categories of issues, and detailed descriptions of the issues.'''
    def extract_issue_categories():
        categories = {}
        for k, v in ISSUE_DEFINITIONS.items():
            category = v['category']
            if v['category'] not in categories:
                categories[v['category']] = []
            categories[v['category']].append(v['id'])
        result = []
        for k, v in categories.items():
            result.append({
                'id': k, 
                'label': k.title(),
                'issues': v 
            })
        return result
    auto = []
    auto_results_checklist = []
    issues = get(persistent_id)
    issues_saved = [i for i in issues.get('issues', [])] if issues else []
    result = {
        'details': [i for i in ISSUE_DEFINITIONS.values()],
        'auto': auto,
        'manual_checklist': issues_saved, 
        'auto_checklist': auto_results_checklist,
        'categories': extract_issue_categories()
    }
    return result


def set(issue_list: IssueList, user_id: Optional[str]=None):
    '''Updates the checklist for the dataset issues. If persistent_id/issues does not exist in fs, creates the folder/file. 
        Returns True if successful.'''
    dataset_id = filesystem.get_foldername_from_persistent_id(issue_list.persistent_id)
    file_path = [dataset_id, 'issues']
    base_dir = filesystem.BASE_DIR.copy()
    for folder in file_path:
        if not folder in os.listdir(os.path.join(*base_dir)):
            logging.info(f'adding {folder} to {os.listdir(os.path.join(*base_dir))}')
            os.mkdir(os.path.join(*base_dir, folder))
        base_dir.append(folder)
    issues_file = shelve.open(os.path.join(*base_dir, 'checklist_state'))
    try:
        issues_file.update(issue_list.__dict__)
        result = True
    except:
        result = False
    finally:
        issues_file.close()
    return result

def get(persistent_id: str) -> IssueList:
    '''Reads the previously saved checklist for the dataset issues. Returns None if not found.'''
    file_path = os.path.join(*filesystem.BASE_DIR, filesystem.get_foldername_from_persistent_id(persistent_id), 'issues', 'checklist_state')
    issues = None
    try:
        issues = shelve.open(file_path)
        result = dict(issues).copy()
        return result
    except Exception:
        return None
    finally:
        if issues is not None:
            try:
                issues.close()
            except Exception:
                pass


async def generate_feedback_email(persistent_identifier):
    """Generates a feedback email for the dataset contributor, based on previously saved issues checklist. The template in emails/feedback.txt and issue definitions in dataset_issue_definitions.json are used."""
    dataset_details = await metadata.async_get_dataset_details(persistent_identifier)
    author_names = ', '.join([author_name.split(',')[-1].strip() for author_name in dataset_details.get('authorName', [])])
    
    try:
        reviewer_username = dataset_details.get('reviewer')[0]
        reviewer_info = await user.get_user_info(reviewer_username)
    except:
        reviewer_info = {}
    reviewer_name = reviewer_info.get('userfirstname', '')
    issue_details = await get_details(persistent_identifier)
    excluded_issues = []
    excluded_issues.extend(issue_details.get('auto_checklist'))
    excluded_issues.extend(issue_details.get('manual_checklist'))
    issue_definitions = [issue.get('message') for issue in issue_details.get('details') if issue.get('id') not in excluded_issues]
    issues_list = "\n".join([f"{num+1}. {issue}\n" for num, issue in enumerate(issue_definitions)])
    dataset_title = dataset_details.get('title')
    message = FEEDBACK_EMAIL
    for k, v in {"{author_names}": author_names, "{dataset_title}":dataset_title, "{issues_list}":issues_list, "{reviewer_name}":reviewer_name}.items():
        message = message.replace(k, v)
    return message