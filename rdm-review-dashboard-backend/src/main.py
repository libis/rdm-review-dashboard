from pathlib import Path
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import os
from utils.logging import logging
import utils.logging
from utils import response_headers


import json
from services.dataverse import native
from services.dataverse import solr
from services import email
from services import issue
from persistence import filesystem
from services.dataverse import user
from views import home, datasets, reviewer, status, notes, support, feedback
from fastapi.staticfiles import StaticFiles
from services.dataverse import postgresql
import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


SETTINGS_FILE = ""
DATAVERSE_API_KEY = None
UI_PATH = None

api = fastapi.FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.middleware("http")
async def redirect_to_index(request: fastapi.Request, call_next):
    response = await call_next(request)
    if (
        not UI_PATH
        or request.url.path.startswith("/api/")
        or response.status_code != 404
    ):
        return response
    return fastapi.responses.HTMLResponse(
        content=open(UI_PATH + "/index.html", "r").read(), status_code=200
    )


def configure():
    global SETTINGS_FILE
    global UI_PATH
    global api
    SETTINGS_FILE = (
        os.environ.get("BACKEND_CONFIG_FILE") or "./config/backend_config.json"
    )

    settings = load_settings_file(SETTINGS_FILE)
    filesystem.BASE_DIR = [settings.get("dataPath")]
    utils.logging.configure_logging()

    configure_routing()

    configure_api_keys(settings)
    native.wait_dataverse()
    configure_email(settings)
    configure_postgresql(settings)
    configure_authentication(settings)
    solr.BASE_URL = get_setting(settings, "SolrHost", required=True) + "/solr"
    if get_setting(settings, "SolrAPIKeyFile"):
        solr.KEY = read_value_from_file(get_setting(settings, "SolrAPIKeyFile"), required=False)

    configure_dataset_issue_definitions(settings)
    try:
        with open(get_setting(settings, "emailTemplatesPath", required=True) + "/feedback.txt") as f:
            issue.FEEDBACK_EMAIL = f.read()
    except Exception as e:
        logging.info(e)
        raise e

    # configure_users(settings)

    UI_PATH = get_setting(settings, "UIPath", required=True)
    if UI_PATH:
        api.mount("/ui/", StaticFiles(directory=UI_PATH), name="ui")


def configure_routing():
    api.include_router(home.router)
    api.include_router(reviewer.router)
    api.include_router(status.router)
    api.include_router(notes.router)
    api.include_router(feedback.router)
    api.include_router(support.router)
    api.include_router(datasets.router)


def configure_authentication(settings):
    response_headers.ROLES = get_setting(settings, "reviewerRoles", required=True)
    response_headers.USERID_HEADER_FIELD = get_setting(settings, "userIdHeaderField")
    user.GROUP_ALIASES = get_setting(settings, "dataverseUserGroupAliases", required=True)


def configure_dataset_issue_definitions(settings):
    issues = load_settings_file(
        Path(get_setting(settings, "issueDefinitionsFile", required=True)).absolute()
    )
    issue.ISSUE_DEFINITIONS = issues


def configure_postgresql(settings):
    pg_host = get_setting(settings, "PostgresHost", required=True)
    pg_port = get_setting(settings, "PostgresPort", required=True)
    pg_password_file = get_setting(settings, "PostgresPasswordFile", required=True)
    pg_db = get_setting(settings, "PostgresDB", required=True)
    pg_user = get_setting(settings, "PostgresUser", required=True)
    pg_password = read_value_from_file(pg_password_file, required=True)
    postgresql.conn = postgresql.get_connection(
        pg_host, pg_port, pg_db, pg_user, pg_password
    )
    lock = threading.Lock()
    with lock:
        for view_name in ["datasetversion_info", "datasetversion_metadata"]:
            result = postgresql.add_view(view_name, pg_user)
            if result:
                logging.info(f"PostgreSQL view {view_name} added successfully.")
                continue


def load_settings_file(file_path):
    result = None
    try:
        with open(file_path) as f:
            result = json.load(f)
    except:
        raise
    return result


def read_value_from_file(file_path, required=False):
    file = Path(file_path).absolute()
    if not file.exists():
        if required:
            logging.info(f"{file_path} file not found.")
            raise FileNotFoundError
        return None
    with open(file) as f:
        return f.readline().strip()


def get_setting(settings, setting_name, required=False):
    if required and setting_name not in settings:
        raise Exception(f"Required setting {setting_name} not found...")
    result = settings.get(setting_name)
    logging.info(f"{setting_name} : {result}")
    return result


def configure_email(settings):
    email.SMTP_HOST = get_setting(settings, "SMTPHost", required=True)
    email.SMTP_PORT = get_setting(settings, "SMTPPort", required=True)
    if get_setting(settings, "SMTPPasswordFile"):
        email.SMTP_PASSWORD = read_value_from_file(get_setting(settings, "SMTPPasswordFile"), required=True)
    email.RDM_HELPDESK_EMAILS = get_setting(settings, "helpdeskEmails", required=True)
    email.TEST_EMAIL = get_setting(settings, "testEmail")


def configure_api_keys(settings):
    email.DATAVERSE_URL = get_setting(settings, "DataverseURL", required=True)
    native.BASE_URL = get_setting(settings, "DataverseAPI", required=True) + "/api"
    native.KEY = read_value_from_file(get_setting(settings, "DataverseAPIKeyFile", required=True))


def configure_users(settings):
    user_file_path = Path(get_setting(settings, "usersFile")).absolute()
    if user_file_path.exists():
        with open(user_file_path) as f:
            admins = []
            users_ = json.load(f)
            for k, v in users_.items():
                if v.get("isAdmin"):
                    admins.append(k)
            user.ADMINS = admins
            user.USERS = users_


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="0.0.0.0")
else:
    configure()
