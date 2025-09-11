import psycopg2
from utils.logging import logging
from utils.generic import read_value_from_file

HOST = ""
PORT = ""
DATABASE = ""
USER = ""
PASSWD_FILE = ""


def get_password():
    global PASSWD_FILE
    return read_value_from_file(PASSWD_FILE)

def test_connection():
    logging.info(
        f"Testing connection to PostgreSQL database: {HOST}:{PORT} {DATABASE}"
    )
    result = False
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            result = db_version[0]
            logging.info(
                f"Connection to PostgreSQL database successful. DB version: {result}"
            )
    except Exception as e:
        logging.error(f"Connection to PostgreSQL database failed: {e}")
    finally:
        if conn:
            conn.close()
    return result


def get_connection():
    """Returns a connection to the specified PostgreSQL database."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USER,
            password=get_password(),
            connect_timeout=10,
        )
        # Avoid idle-in-transaction sessions blocking DDL by defaulting to autocommit
        conn.autocommit = True
        # Apply conservative timeouts to minimize long blocking
        with conn.cursor() as _cur:
            try:
                _cur.execute("SET lock_timeout TO '5s';")
                _cur.execute("SET statement_timeout TO '60s';")
            except Exception as e:
                # Non-fatal: log and proceed; some roles may not allow SET
                logging.debug(f"Could not set connection timeouts: {e}")
    except Exception as e:
        logging.info(f"Could not connect to PostgresSQL: {e}")
        raise
    return conn

def query_locks():
    """Returns all dataset locks."""
    query = """SELECT  ds.id, 
                    datasetlock.reason AS lock, 
                    datasetlock.starttime AS lock_starttime, 
                    datasetlock.user_id AS lock_user_id 
                FROM dataset AS ds 
                LEFT join datasetlock ON ds.id = datasetlock.dataset_id;"""
    return run_query(query)

def run_query(query):
    """Establishes a connection to the database, runs the query and closes the connection. 
    Returns the results in a list of dictionaries, consisting of column name and data. """
    conn = None
    result = []
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            while row:
                cols = [description_item[0] for description_item in cur.description]
                if row:
                    new_record = {col: content for col, content in zip(cols, row)}
                    result.append(new_record)
                row = cur.fetchone()
    except Exception as e:
        logging.error(f"PostgreSQL query failed: {e}")
        raise
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
    return result

def query_dataset_metadata(authority=None, identifier=None):
    """Returns metadata for a dataset.
    
    Returns:
    PostgreSQL cursor.
    """
    query = f"""SELECT
        datasetversion_info.*,
        metadata.metadata
    FROM datasetversion_info
    LEFT JOIN (
        SELECT 
            version_id,
            jsonb_object_agg(name, COALESCE(value, NULL)) AS metadata
        FROM datasetversion_metadata

        GROUP BY version_id
    ) metadata ON metadata.version_id = datasetversion_info.version_id
    WHERE authority='{authority}' AND identifier='{identifier}'
    ;
    """
    return run_query(query)


def query_datasets_metadata(start=None, rows=None, status=None, reviewer=None):
    """Returns the cursor for querying metadata for datasets with the given filtering and paging arguments.
    Args:
    status (Optional str): filter datasets by status.
    reviewer (Optional str): filter datasets by reviewer assignment.

    start (Optional int): starting row.
    rows (Optional int): number of rows retrieved.

    Returns:
    PostgreSQL cursor.
    """
    status_query = None
    if status:
        if status == "draft":
            status_query = (
                "versionstate='DRAFT' AND array_position(locks, 'InReview') IS null"
            )
        if status == "in_review":
            status_query = "versionstate='DRAFT' AND array_position(locks, 'InReview') IS NOT null AND reviewers IS NOT null"
        if status == "submitted_for_review":
            status_query = "versionstate='DRAFT' AND array_position(locks, 'InReview') IS NOT null AND reviewers IS null"
        if status == "published":
            status_query = "versionState='RELEASED'"

    assigned_to_query = None
    if reviewer:
        assigned_to_query = f"array_position(reviewers, '{reviewer}') IS NOT null"

    query = f"""SELECT
        datasetversion_info.*,
        metadata.metadata
    FROM datasetversion_info
    LEFT JOIN (
        SELECT 
            version_id,
            jsonb_object_agg(name, COALESCE(value, NULL)) AS metadata
        FROM datasetversion_metadata

        GROUP BY version_id
    ) metadata ON metadata.version_id = datasetversion_info.version_id
    {'WHERE' if status_query or assigned_to_query else ''}
    {status_query if status_query else ''}
    {'AND' if status_query and assigned_to_query else ''}
    {assigned_to_query if assigned_to_query else ''}
    {'LIMIT ' + str(rows) if isinstance(rows, int) else ''}
    {'OFFSET ' + str(start) if isinstance(start, int) else ''}
    ;
    """
    return run_query(query)


def query_dataverse_user_info(user_id):
    query = f"""SELECT explicitgroup.id AS groupId, 
        explicitgroup.groupaliasinowner AS groupAliasInOwner, 
        explicitgroup.owner_id AS groupOwnerId, 
        explicitgroup.description AS groupDescription, 
        explicitgroup.displayname AS groupDisplayName, 
        authenticateduser.useridentifier AS userName,
        authenticateduser.position AS userPosition,
        authenticateduser.email AS userEmail,
        authenticateduser.affiliation AS userAffiliation,
        authenticateduser.superuser AS userSuperUser,
        authenticateduser.firstname AS userFirstName,
        authenticateduser.lastname AS userLastName
        FROM authenticateduser 
        LEFT JOIN public.explicitgroup_authenticateduser ON explicitgroup_authenticateduser.containedauthenticatedusers_id=authenticateduser.id
        LEFT JOIN public.explicitgroup
        ON explicitgroup.id=explicitgroup_authenticateduser.explicitgroup_id
        WHERE authenticateduser.useridentifier=\'{user_id.strip('@')}\';
        """
    return run_query(query)


def query_dataverse_users(group_aliases=None):
    group_id_clause = None
    if group_aliases:
        joint_ids = ", ".join(["'" + group_alias + "'" for group_alias in group_aliases])
        group_id_clause = f"WHERE groupAliasInOwner=ANY(ARRAY[{joint_ids}])"
    query = f"""SELECT explicitgroup.id AS groupId, 
            explicitgroup.groupaliasinowner AS groupAliasInOwner, 
            explicitgroup.owner_id AS groupOwnerId, 
            explicitgroup.description AS groupDescription, 
            explicitgroup.displayname AS groupDisplayName, 
            authenticateduser.useridentifier AS userName,
            authenticateduser.position AS userPosition,
            authenticateduser.email AS userEmail,
            authenticateduser.affiliation AS userAffiliation,
            authenticateduser.superuser AS userSuperUser,
            authenticateduser.firstname AS userFirstName,
            authenticateduser.lastname AS userLastName
            FROM public.explicitgroup 
            LEFT JOIN public.explicitgroup_authenticateduser 
            ON explicitgroup.id=explicitgroup_authenticateduser.explicitgroup_id
            LEFT JOIN authenticateduser ON explicitgroup_authenticateduser.containedauthenticatedusers_id=authenticateduser.id
            {group_id_clause if isinstance(group_id_clause, str) else ''};
        """
    return run_query(query)


def query_dataset_review_status_counts(reviewer=None):
    assigned_to_query = None
    if reviewer:
        assigned_to_query = f"WHERE array_position(reviewers, '{reviewer}') IS NOT null"
    query = f"""SELECT count(identifier) AS datasetCount, 
            versionstate,
            CASE WHEN (reviewers IS NOT null) THEN true ELSE false END AS hasReviewer,
            CASE WHEN (array_position(locks, 'InReview') IS NOT null) THEN true ELSE false END AS inReview 
            from datasetversion_info 
            {assigned_to_query if assigned_to_query else ''}
            GROUP BY versionState, inReview, hasReviewer;"""
    return run_query(query)


def view_exists(view_name):
    """Checks if a view is already present in the database."""
    query = f"""SELECT EXISTS (
                SELECT *
                FROM information_schema.views
                WHERE table_name = '{view_name}'
                );"""
    result = None
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            postgres_result = cur.fetchone()
            try:
                result = postgres_result[0]
            except Exception:
                result = None
                raise Exception(f"View check in postgres returned: {postgres_result}")
    except Exception as e:
        logging.error(f"Failed to check view existence for {view_name}: {e}")
        raise
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
    return result


def add_view(view_name):
    """Checks if a view is present in the database and adds it if not."""
    if view_exists(view_name):
        logging.info(f"PosgreSQL view {view_name} already exists.")
        return False

    query = None
    file_path = f"sql/views/{view_name}.sql"

    with open(file_path) as file:
        query = file.read()
    if not query:
        raise Exception(f"Could not read query {file_path}")
    query = query.replace("__db_username__", USER)
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            logging.debug(f"Adding view: {view_name} with query: {query}")
            cur.execute(query)
            # autocommit is enabled; explicit commit is a no-op but harmless
            try:
                conn.commit()
            except Exception:
                pass
    except Exception as e:
        logging.critical(f"{view_name} could not be added: {e}")
        raise
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

    if not view_exists(view_name):
        raise Exception(f"PostgreSQL view {view_name} could not be added.")
    logging.info(f"PostgreSQL view {view_name} added successfully.")
    return True


def query_dataset_assignments(authority: str, identifier: str):
    """Returns all the assignments and their user info (firstname, lastname, affiliation, email) defined on the latest version of a dataset."""
    query = f"""SELECT * FROM datasetversion_info LEFT JOIN roleassignment ON roleassignment.definitionpoint_id = datasetversion_info.dataset_id
	LEFT JOIN authenticateduser ON authenticateduser.useridentifier=SUBSTRING(roleassignment.assigneeidentifier FROM 2) 
    LEFT JOIN dataverserole ON roleassignment.role_id=dataverserole.id
	WHERE datasetversion_info.authority='{authority}' AND datasetversion_info.identifier='{identifier}';"""
    return run_query(query)
