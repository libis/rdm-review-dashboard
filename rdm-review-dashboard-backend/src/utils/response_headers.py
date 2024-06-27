from functools import wraps
from services.dataverse import user

USERID_HEADER_FIELD = ""
ROLES = []


async def has_authorized_role(user_id):
    """Checks if a user has access to the API, based on their role in Dataverse."""
    user_roles = await user.get_user_roles(user_id)
    for role in ROLES:
        if user_roles.get(f"is{role.capitalize()}"):
            return True
    return False


def inject_uid(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Reads the username from the request header and adds it to the response headers.
        This decorator will not work if 'request' and 'response' are not in the kwargs of the
        wrapped call!"""
        uid = kwargs.get("request").headers.get(USERID_HEADER_FIELD)
        if uid and await has_authorized_role(uid):
            kwargs["response"].headers["X-User"] = uid
            return await func(*args, **kwargs)
        return "Not authorized."
    return wrapper
