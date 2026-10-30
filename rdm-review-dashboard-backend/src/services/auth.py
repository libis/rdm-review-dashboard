from typing import List
from services.dataverse import user
from utils.logging import logging
from fastapi import HTTPException



async def get_user_groups(user_id):
    groups = await user.get_user_groups(user_id)
    result = []
    for group, membership in groups.items():
        if membership:
            result.append(group.removeprefix("is").lower())
    return result


async def require_group(user_groups, groups_allowed):
    """Checks if a group has access to the API, based on their role in Dataverse."""
    for user_group in user_groups:
        if user_group in groups_allowed:
            return True
    raise HTTPException(status_code=404, detail=f"User does not have access to this endpoint.")

async def require_dataset_assignment(user_id: str, roles: List[str], dataset_id: str, version: str = None):
    result = await check_dataset_assignment(user_id, roles, dataset_id, version)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"User '{user_id}' does not have access to this dataset'.")

async def check_dataset_assignment(user_id: str, roles: List[str], dataset_id: str, version: str = None):
    assignments = await user.get_assigned_datasets(user_id, roles)
    for assignment in assignments:
        if assignment.get("role") in roles \
            and assignment.get("identifier") == dataset_id \
            and (not version or assignment.get("version") == version):
                return assignment
    return None

async def require_group_and_assignment(user_id: str, assignment_requirements: dict):
    
    required_groups = assignment_requirements.keys()
    user_groups = await get_user_groups(user_id)

    if not await require_group(user_groups, required_groups):
        raise HTTPException(status_code=404, detail=f"User '{user_id}' does not have access to this endpoint'.")
    
    for group_name, assignment_requirement in assignment_requirements.items():

        if group_name in user_groups:
            if assignment_requirement  == None:
                return True
            else:
                role = assignment_requirement.get("role")
                _object = assignment_requirement.get("object")
                object_type = _object.get("type")
                object_id = _object.get("id")
                match object_type:
                    case "dataset":
                        version = _object.get("version")
                        if await check_dataset_assignment(user_id, [role], object_id, version):
                            return True
                        logging.error(f"User {user_id} is not assignned to {object_type}: {object_id} as {role}")
                    case _:
                        logging.error("Object type not supported: {object_type}")
    raise HTTPException(status_code=404, detail=f"Unknown authorization error.")


