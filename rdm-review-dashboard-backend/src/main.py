from pathlib import Path
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import os
import shutil
from utils.logging import logging
import utils.logging
from utils import response_headers
from utils.generic import read_value_from_file

import json
from services.dataverse import native
from services.dataverse import solr
from services import email
from services import issue
from persistence import filesystem
from services.dataverse import user
from views import home, datasets, reviewer, status, notes, support, feedback
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

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
    UI_BASE_HREF = get_setting(settings, "UI_BASE_HREF", required=False) or "/ui/"
    UI_ASSETS_PATH = get_setting(settings, "UIAssetsPath", required=False)

    if UI_ASSETS_PATH:
        api.mount("/ui/assets/", StaticFiles(directory=UI_ASSETS_PATH), name="assets")

    if UI_PATH:
        api.mount(UI_BASE_HREF, StaticFiles(directory=UI_PATH, html=True), name="ui")

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
    postgresql.HOST = get_setting(settings, "PostgresHost", required=True)
    postgresql.PORT = get_setting(settings, "PostgresPort", required=True)
    postgresql.PASSWD_FILE = get_setting(settings, "PostgresPasswordFile", required=True)
    postgresql.DATABASE = get_setting(settings, "PostgresDB", required=True)
    postgresql.USER = get_setting(settings, "PostgresUser", required=True)
    postgresql.test_connection()

    lock = threading.Lock()
    with lock:
        for view_name in ["datasetversion_info", "datasetversion_metadata"]:
            result = postgresql.add_view(view_name)
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
    # Bind host is configurable; default to loopback for local safety.
    _host = os.getenv("UVICORN_HOST", "127.0.0.1")
    _port = int(os.getenv("UVICORN_PORT", "8000"))
    uvicorn.run(api, port=_port, host=_host)
else:
    configure()
