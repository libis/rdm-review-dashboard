from utils import request_utils
import json
from typing import Optional, Literal
from utils.logging import logging
from requests import Response
BASE_URL = ''
KEY = ''


def wait_dataverse():
    """Waits until dataverse API responds."""
    request_url = f'{BASE_URL}/info/version'
    response = None
    while not isinstance(response, Response)  or response.status_code != 200:
        response = request_utils.get_request(request_url)

def retrieve_dataset_assignees(persistent_id):
    """Retrieves all assignments of the dataset."""
    request_url = f'{BASE_URL}/datasets/:persistentId/assignments'
    response = request_utils.get_request(request_url, KEY, persistentId=persistent_id)
    
    return response

def assign_role(persistent_id, user_id, role_alias):
    """Assigns the user_id to the dataset with the role alias."""
    if user_id:
        user_id = '@' + user_id.strip('@')
    request_url = f'{BASE_URL}/datasets/:persistentId/assignments'
    json_dict = {
        "assignee": user_id,
        "role": role_alias
        }
    
    response = request_utils.post_request(request_url, KEY, json_dict=json_dict, persistentId=persistent_id)
    return response

def delete_roles(persistent_id, user_id, role_aliases):
    """Deletes the user_id or the given role aliases from the dataset"""
    response = retrieve_dataset_assignees(persistent_id)
    res = None

    if response.status_code == 200:
        assignees = json.loads(response.text).get('data', [])
        if user_id:
            user_id = '@' + user_id.strip('@')
        # logging.info(assignees)
        for assignee in assignees:
            if  ((user_id and assignee.get('assignee') == user_id) or not user_id) and assignee.get('_roleAlias') in role_aliases:
                _id = assignee.get('id')
                url=f'{BASE_URL}/datasets/:persistentId/assignments/{_id}?persistentId={persistent_id}'
                res = request_utils.delete_request(url, key=KEY)
    return res

async def submit_for_review(dataset_id):
    """Submits the dataset for review."""
    request_url = f'{BASE_URL}/datasets/:persistentId/submitForReview'
    response = await request_utils.async_post_request(request_url, key=KEY, data={'persistentId': dataset_id})
    return response

async def publish(dataset_id, version=Optional[Literal['minor', 'major', 'updateCurrent']]):
    """Publishes the dataset, with the provided version number increase."""
    if not version:
        version = 'major'
    request_url = f'{BASE_URL}/datasets/:persistentId/actions/:publish'
    response = await request_utils.async_post_request(request_url, key=KEY, persistentId=dataset_id, type=version)
    
    return response

async def return_to_author(dataset_id, feedback=None):
    """Returns the specified dataset to author with the indicated feedback if available."""
    request_url = f'{BASE_URL}/datasets/:persistentId/returnToAuthor'
    json_dict = {
                "reasonForReturn": feedback
            }
    response = await request_utils.async_post_request(request_url, key=KEY, json_dict=json_dict, persistentId=dataset_id)
    return response

async def async_retrieve_dataset_assignees(persistent_id: str):
    """Retrieves all assignments of the dataset."""
    request_url = f'{BASE_URL}/datasets/:persistentId/assignments'
    response = await request_utils.async_get_request(request_url, KEY, persistentId=persistent_id)
    return response

async def async_retrieve_dataset_details(dataset_id: str):
    request_url =  f'{BASE_URL}/datasets/:persistentId' 
    response = await request_utils.async_get_request(request_url, key=KEY, persistentId=dataset_id)
    return response

def retrieve_dataset_details(dataset_id: str):
    request_url =  f'{BASE_URL}/datasets/:persistentId' 
    response = request_utils.get_request(request_url, key=KEY, persistentId=dataset_id)
    return response

async def async_retrieve_dataset_versions(dataset_id: str):
    request_url =  f'{BASE_URL}/datasets/{dataset_id}/versions' 
    response = await request_utils.async_get_request(request_url, key=KEY)
    return response

async def retrieve_dataset_locks(persistent_id: str):
    request_url =  f'{BASE_URL}/datasets/:persistentId/locks?persistentId={persistent_id}' 
    response = await request_utils.async_get_request(request_url, key=KEY)
    return response

async def retrieve_all_dataset_locks():
    request_url =  f'{BASE_URL}/datasets/locks' 
    response = await request_utils.async_get_request(request_url, key=KEY)
    return response