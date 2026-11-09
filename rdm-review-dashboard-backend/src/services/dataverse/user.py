import json
from typing import List
from services.dataverse import postgresql
from utils.logging import logging
from fastapi import HTTPException

GROUP_ALIASES = {}
USERS = {}
ADMINS = []


async def get_user_info(user_id: str) -> dict:
    """Retrieves author information from Dataverse."""
    result = {}
    user_id = user_id.strip(" ")
    user_id = user_id.strip("@")
    rows = postgresql.query_dataverse_user_info(user_id)

    for row in rows:
        new_record = await format_user_data(row)
        result = result or new_record
        if new_record["isReviewer"] == True:
            result["isReviewer"] = True
        if new_record["isAdmin"] == True:
            result["isAdmin"] = True
        first_name = new_record.get("userfirstname")
        last_name = new_record.get("userlastname")
        result["name"] = first_name or ""
        if result["name"] and last_name:
            result["name"] += " "
        if last_name:
            result["name"] += last_name
        if not result["name"]:
            result["name"] = result["username"]
    return result


async def get_user_groups(user_id: str) -> dict:
    """Returns the roles of the user."""
    dataverse_user_id = user_id.strip("@")
    rows = postgresql.query_dataverse_user_info(dataverse_user_id)
    result = {}
    user_groupaliases = set()
    for row in rows:
        if result == {} and row:
            result = row
        if group_alias := row.get("groupaliasinowner"):
            user_groupaliases.add(group_alias)
    for group_name, group_aliases in GROUP_ALIASES.items():
        result[f"is{group_name.capitalize()}"] = (
            result.get(f"is{group_name.capitalize()}")
            or user_groupaliases.intersection(set(group_aliases)) != set()
        )
    result.update(USERS.get("@" + user_id, {}))
    return result

async def get_user_data(user_id: str) -> dict:
    """Returns the roles of the user."""
    dataverse_user_id = user_id.strip("@")
    
    rows = postgresql.query_dataverse_user_info(dataverse_user_id)
    return rows


async def format_user_data(record):
    """Adds the fields isAdmin and isReviewer to the user record based on user roles in Dataverse and settings."""
    alias = record.get("groupaliasinowner")
    isUserAdmin = alias in GROUP_ALIASES["admin"]
    isUserReviewer = alias in GROUP_ALIASES["reviewer"]
    record.update(
        {
            "isAdmin": isUserAdmin,
            "isReviewer": isUserReviewer or isUserAdmin,
        }
    )
    return record


async def get_dataverse_assignees(groups=None) -> List[dict]:
    """Returns a list of users that are assigned to the RDR dataverse, and their roles."""
    group_aliases = set()
    for group in groups:
        group_aliases = group_aliases.union(set(GROUP_ALIASES.get(group, [])))

    users = {}
    rows = postgresql.query_dataverse_users(group_aliases=list(group_aliases))
    for row in rows:
        new_record = await format_user_data(row)
        username = new_record.get("username")
        user = users.get(username) or new_record
        if new_record["isReviewer"] == True:
            user["isReviewer"] = True
        if new_record["isAdmin"] == True:
            user["isAdmin"] = True

        users[username] = user

    users_from_file = {k.strip("@"): v for k, v in USERS.items()}
    usernames = set(users_from_file.keys()).union(set(users.keys()))
    for username in usernames:
        users[username] = users.get(username, {})
        users[username].update(users_from_file.get(username, {}))
    return list(users.values())


async def get_dataset_assignment(user_id: str, roles: List[str], persistent_id: str=None, only_drafts=False, allow_indirect=False):
    """Returns the user's assignments on one dataset, direct or inherited from a parent collection."""
    authority = persistent_id.split("/")[0].replace("doi:", "")
    identifier = "/".join(persistent_id.split("/")[1:])
    rows = postgresql.query_direct_assignments(user_id, roles)
    if allow_indirect:
        rows_indirect = postgresql.query_indirect_assignments(user_id, roles)
        rows.extend(rows_indirect)
    result = []
    if not persistent_id:
        result = rows
    else:
        for row in rows:
            if row.get("authority") == authority and row.get("identifier") == identifier:
                if not only_drafts or row.get("versionstate") == "DRAFT":
                    result.append(row)
    return result


async def get_assigned_datasets(user_id: str, roles: List[str]):
    query_results = postgresql.query_user_assignments(user_id, roles)
    result = []
    for dataset in query_results:
        version = None
        if dataset.get("versionnumber") or dataset.get("minorversionnumber"):
            version = f"{dataset.get('versionnumber') or 0}.{dataset.get('minorversionnumber') or 0}"
        else:
            version = "DRAFT"
        result.append(
            {
                "identifier": f"doi:{dataset.get("authority")}/{dataset.get("identifier")}",
                "version": version,
                "role": f"{dataset.get("alias")}",
                "title": f"{dataset.get("value")[0]}",
            }
        )
    return result 