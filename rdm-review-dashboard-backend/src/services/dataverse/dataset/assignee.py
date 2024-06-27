from services.dataverse import native
import json
from utils.logging import logging

def get_dataset_assignees(persistent_id):
    """
    Retrieves a dataset's assignees, in a dictionary in a dictionary:

    Args: 
        persistent_id (str): persistent id of the dataset

    Returns:
        dict:
            {"_roleAlias": ["user1id", "user2id"...], 
                ...
            }
    """
    response = native.retrieve_dataset_assignees(persistent_id)
    result = {}
    if response.status_code == 200:
        assignees = json.loads(response.text).get('data', [])
        for assignee in assignees:
            assignee_id = assignee.get('assignee')
            if assignee_id.startswith("&"):
                continue
            alias = assignee.get('_roleAlias')
            if alias not in result:
                result[alias] = []
            result[alias].append(assignee_id)
    return result


def set_reviewer(persistent_id, user_id):
    """Assign a user to a dataset with the reviewer role."""
    response = native.assign_role(persistent_id, user_id, 'reviewer')
    return response


def delete_reviewer(persistent_id, user_id):
    response = native.delete_roles(persistent_id, user_id, ['reviewer'])
    return response


def delete_all_reviewers(persistent_id):
    response = native.delete_roles(persistent_id, None, ['reviewer'])
    return response