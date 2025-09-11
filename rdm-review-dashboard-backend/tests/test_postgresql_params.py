import pytest
from unittest.mock import patch, MagicMock

import services.dataverse.postgresql as pg


@pytest.fixture(autouse=True)
def configure_pg(monkeypatch):
    monkeypatch.setattr(pg, 'HOST', 'localhost')
    monkeypatch.setattr(pg, 'PORT', '5432')
    monkeypatch.setattr(pg, 'DATABASE', 'db')
    monkeypatch.setattr(pg, 'USER', 'user')
    monkeypatch.setattr(pg, 'PASSWD_FILE', '/tmp/secret')
    monkeypatch.setattr(pg, 'read_value_from_file', lambda path, required=True: 'pwd')


def make_conn_cursor():
    cur = MagicMock()
    cur.__enter__.return_value = cur
    cur.__exit__.return_value = False
    conn = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_query_dataset_metadata_is_parameterized(mock_connect):
    conn, cur = make_conn_cursor()
    # minimal result to terminate loop inside run_query
    cur.description = [('a',)]
    cur.fetchone.side_effect = [None]
    mock_connect.return_value = conn

    pg.query_dataset_metadata('AUTH', 'ID')
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert '%s' in sql and 'AUTH' not in sql and 'ID' not in sql
    assert params == ('AUTH', 'ID')


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_query_datasets_metadata_filters_and_paging(mock_connect):
    conn, cur = make_conn_cursor()
    cur.description = [('x',)]
    cur.fetchone.side_effect = [None]
    mock_connect.return_value = conn

    pg.query_datasets_metadata(start=5, rows=10, status='in_review', reviewer='@u')
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert 'array_position(reviewers, %s)' in sql
    assert 'LIMIT %s' in sql and 'OFFSET %s' in sql
    assert params == ('@u', 10, 5)


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_query_dataverse_user_info_paramized(mock_connect):
    conn, cur = make_conn_cursor()
    cur.description = [('x',)]
    cur.fetchone.side_effect = [None]
    mock_connect.return_value = conn

    pg.query_dataverse_user_info('@name')
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert 'WHERE authenticateduser.useridentifier = %s' in sql
    assert params == ('name',)


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_query_dataverse_users_any_param(mock_connect):
    conn, cur = make_conn_cursor()
    cur.description = [('x',)]
    cur.fetchone.side_effect = [None]
    mock_connect.return_value = conn

    pg.query_dataverse_users(['grp1', 'grp2'])
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert 'groupaliasinowner = ANY(%s)' in sql
    assert params == (['grp1', 'grp2'],)


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_query_dataset_review_status_counts_param(mock_connect):
    conn, cur = make_conn_cursor()
    cur.description = [('x',)]
    cur.fetchone.side_effect = [None]
    mock_connect.return_value = conn

    pg.query_dataset_review_status_counts('user1')
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert 'array_position(reviewers, %s)' in sql
    assert params == ('user1',)


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_view_exists_paramized(mock_connect):
    conn, cur = make_conn_cursor()
    cur.fetchone.return_value = [True]
    mock_connect.return_value = conn

    assert pg.view_exists('v1') is True
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert 'WHERE table_name = %s' in sql
    assert params == ('v1',)


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_query_dataset_assignments_paramized(mock_connect):
    conn, cur = make_conn_cursor()
    cur.description = [('x',)]
    cur.fetchone.side_effect = [None]
    mock_connect.return_value = conn

    pg.query_dataset_assignments('AUTH', 'ID')
    sql, params = cur.execute.call_args[0][0], cur.execute.call_args[0][1]
    assert 'WHERE datasetversion_info.authority=%s AND datasetversion_info.identifier=%s' in sql
    assert params == ('AUTH', 'ID')
