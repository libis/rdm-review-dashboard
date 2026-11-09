from typing import List
from services.dataverse import user
from utils.logging import logging
from fastapi import HTTPException
import fastapi
from functools import wraps



USERID_HEADER_FIELD = "Ajp_uid"
ROLES = []



async def check_dataset_assignment(user_id: str, roles: List[str], dataset_id: str, only_drafts: bool = True, allow_indirect=False):
    """Returns the first assignment or None.
    By default, assignments inherited from a parent collection count too;
    with direct_only=True only assignments made on the dataset itself count.
    If version == "DRAFT", the dataset must also have a draft version."""
    assignments = await user.get_dataset_assignment(
        user_id, roles, dataset_id, only_drafts, allow_indirect
    )
    return assignments and len(assignments) > 0


async def get_user_groups(uid):
    user_data = await user.get_user_data(uid)
    user_groups = set()

    for row in user_data:
        if row.get("groupalias"): 
            user_groups.add("&explicit/" + row.get("groupalias"))
        if row.get("groupaliasinowner"):
            user_groups.add(row.get("groupaliasinowner"))
    return user_groups


def require_auth(groups_allowed, assignments_required, allow_indirect_assignments=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                uid = kwargs.get("request").headers.get(USERID_HEADER_FIELD)
            except:
                logging.error("SSO Headers not found.")
                raise HTTPException(status_code=404, detail=f"User not logged in..")
            if not uid:
                logging.info("User not logged in.")
                raise HTTPException(status_code=404, detail="User not logged in.")   


            user_groups = await get_user_groups(uid)
            if set(user_groups).intersection(set(groups_allowed)) == set():
                logging.info(f"User {uid} not authorized.")
                raise HTTPException(status_code=404, detail=f"User '{uid}' not authorized.")
            
            if assignments_required:
                roles = assignments_required.get("roles")
                object = assignments_required.get("object")
                dataset_id = kwargs.get("persistent_identifier")
                match object:

                    case "dataset":
                        if not dataset_id:
                            raise HTTPException(status_code=404, detail=f"User does not have access.")
                        if not await auth_for_dataset(uid, user_groups, dataset_id, False, roles, allow_indirect_assignments):
                            raise HTTPException(status_code=404, detail=f"User does not have access.")
                    
                    case "dataset_draft":
                        if not dataset_id:
                            raise HTTPException(status_code=404, detail=f"User does not have access.")
                        if not await auth_for_dataset(uid, user_groups, dataset_id, True, roles, allow_indirect_assignments):
                            raise HTTPException(status_code=404, detail=f"User does not have access.")
                    
                    case _:
                        logging.warning(f"Not implemented; object: {object}, roles: {roles}, args: {kwargs}")
                        raise HTTPException(status_code=404, detail=f"User does not have access.")
            
            kwargs["response"].headers["X-User"] = uid
            return await func(*args, **kwargs)
        return wrapper
    return decorator

async def auth_for_dataset(uid, user_groups, persistent_identifier, only_drafts, roles, allow_indirect_assignments):
            assignment_check_result = await check_dataset_assignment("@" + uid, roles, persistent_identifier, only_drafts, allow_indirect_assignments)
            if not assignment_check_result:
                for user_group in user_groups:
                    assignment_check_result = await check_dataset_assignment(user_group, roles, persistent_identifier, only_drafts, allow_indirect_assignments)
                    if assignment_check_result:
                        break
            print("result: ", assignment_check_result)
            if not assignment_check_result:
                raise HTTPException(status_code=404, detail=f"User does not have access to this endpoint.")
            return assignment_check_result