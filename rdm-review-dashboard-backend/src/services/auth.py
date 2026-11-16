import re
from functools import wraps
from typing import List, Literal, Optional
from dataclasses import dataclass, field

from fastapi import HTTPException
from services.dataverse import user
from utils.logging import logging

USERID_HEADER_FIELD = ""
_VALID_UID = re.compile(r"^[A-Za-z0-9._@-]+$")

GROUPS = {}
ROLE_ASSIGNMENTS = {}

@dataclass(frozen=True)
class AuthContext:
    uid: str
    groups: frozenset
    rule: Rule


@dataclass(frozen=True)
class Rule:
    group: Literal["adminGroup", "reviewerGroup", "contributorGroup"]                      
    scope: Literal["any", "assignment"]
    object: Optional[Literal["dataset", "datasetDraft"]] = None
    roles: Optional[tuple] = ()
    allow_indirect: bool = False


async def get_user_groups(uid) -> set[str]:
    user_data = await user.get_user_data(uid)
    groups = set()
    for row in user_data:
        if row.get("groupalias"):
            groups.add("&explicit/" + row["groupalias"])
        if row.get("groupaliasinowner"):
            groups.add(row["groupaliasinowner"])
    return groups


async def get_dataverse_roles(roles):
    return [ROLE_ASSIGNMENTS[role] for role in roles]


async def get_dataverse_groups(groups)->set:
    return {GROUPS[group_name] for group_name in groups}


async def check_dataset_assignment(assignees: List[str], roles: List[str], dataset_id: str,
                                   only_drafts: bool = True, allow_indirect: bool = False) -> bool:
    for assignee in assignees:
        assignments = await user.get_dataset_assignment(
            assignee, roles, dataset_id, only_drafts, allow_indirect
        )
        if assignments:
            return True
    return False


async def require_group(user_groups, groups_allowed):
    if not user_groups.intersection(await get_dataverse_groups(groups_allowed)):
        logging.info(f"User not authorized.")
        raise HTTPException(status_code=403, detail="Not authorized.")


async def evaluate_rules(rules, uid, user_groups, dataset_id) -> bool:
    assignees = ["@" + uid, *user_groups]
    for rule in rules:
        if GROUPS[rule.group] not in user_groups:
            continue
        if rule.scope == "any":
            return True
        if rule.scope == "assignment":
            if rule.object =="dataset":
                if not dataset_id:
                    continue
                if await check_dataset_assignment(
                    assignees,
                    await get_dataverse_roles(rule.roles),
                    dataset_id,
                    only_drafts=False,
                    allow_indirect=rule.allow_indirect,
                ):
                    return True
            if rule.object =="datasetDraft":
                if not dataset_id:
                    continue
                if await check_dataset_assignment(
                    assignees,
                    await get_dataverse_roles(rule.roles),
                    dataset_id,
                    only_drafts=True,
                    allow_indirect=rule.allow_indirect,
                ):
                    return True

    return False


def require_auth(*rules: Rule):
    if not rules:
        raise ValueError("At least one rule is required")

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request=None, response=None, **kwargs):
            if request is None or response is None:
                raise RuntimeError("Endpoint must declare 'request' and 'response' parameters.")

            uid = request.headers.get(USERID_HEADER_FIELD)
            if not uid or not _VALID_UID.match(uid):
                raise HTTPException(status_code=401, detail="User not logged in.")
            uid = uid.lstrip("@")

            user_groups = await get_user_groups(uid)
            dataset_id = request.path_params.get("persistent_identifier")

            request.state.uid = uid
            request.state.ugroups = user_groups


            matched = await evaluate_rules(rules, uid, user_groups, dataset_id)
            if not matched:
                logging.info(f"User {uid!r} not authorized.")
                raise HTTPException(status_code=403, detail="Not authorized.")

            ctx = AuthContext(uid=uid, groups=frozenset(user_groups), rule=matched)
            request.state.auth = ctx
            response.headers["X-User"] = uid
            return await func(*args, request=request, response=response, **kwargs)
        return wrapper
    return decorator