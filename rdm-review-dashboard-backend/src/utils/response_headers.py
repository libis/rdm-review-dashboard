from functools import wraps
from services.dataverse import user
from utils.logging import logging
from fastapi import HTTPException

USERID_HEADER_FIELD = ""
ROLES = []


async def require_group(user_id, groups_allowed):
    """Checks if a user has access to the API, based on their role in Dataverse."""
    user_roles = await user.get_user_groups(user_id)
    for role in groups_allowed:
        if user_roles.get(f"is{role.capitalize()}"):
            return True
    return False


def inject_uid(groups_allowed=None):
    groups_allowed = groups_allowed or ROLES
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """Reads the username from the request header and adds it to the response headers.
            This decorator will not work if 'request' and 'response' are not in the kwargs of the
            wrapped call!"""
            uid = kwargs.get("request").headers.get(USERID_HEADER_FIELD)
            if not uid:
                logging.info("User not logged in.")
                raise HTTPException(status_code=404, detail="User not logged in.")   
            if not await require_group(uid, groups_allowed):
                logging.info(f"User {uid} not authorized.")
                raise HTTPException(status_code=404, detail=f"User '{uid}' not authorized.")
            else:
                kwargs["response"].headers["X-User"] = uid
                return await func(*args, **kwargs)
        return wrapper
    return decorator
