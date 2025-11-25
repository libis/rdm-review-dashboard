import builtins
import types
import pytest
from unittest.mock import patch, MagicMock, mock_open

# Import the module under test
import services.dataverse.postgresql as pg


@pytest.fixture(autouse=True)
def configure_pg_settings(monkeypatch):
    monkeypatch.setattr(pg, 'HOST', 'localhost')
    monkeypatch.setattr(pg, 'PORT', '5432')
    monkeypatch.setattr(pg, 'DATABASE', 'db')
    monkeypatch.setattr(pg, 'USER', 'user')
    monkeypatch.setattr(pg, 'PASSWD_FILE', '/tmp/secret')
    monkeypatch.setattr(pg, 'read_value_from_file', lambda path, required=True: 'pwd')


def make_conn_cursor_mocks():
    """Create connection and cursor mocks supporting context manager protocol."""
    cur = MagicMock()
    cur.__enter__.return_value = cur
    cur.__exit__.return_value = False

    conn = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_get_connection_sets_autocommit_and_timeouts(mock_connect):
    conn, cur = make_conn_cursor_mocks()
    mock_connect.return_value = conn

    c = pg.get_connection()

    assert c is conn
    assert conn.autocommit is True
    # Ensure timeout SET statements were attempted
    cur.execute.assert_any_call("SET lock_timeout TO '5s';")
    cur.execute.assert_any_call("SET statement_timeout TO '60s';")
    # Ensure connect called with timeout
    args, kwargs = mock_connect.call_args
    assert kwargs['connect_timeout'] == 10


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_run_query_closes_connection_on_success(mock_connect):
    conn, cur = make_conn_cursor_mocks()
    # Simulate a simple result set
    cur.description = [('id',), ('name',)]
    cur.fetchone.side_effect = [ (1, 'a'), None ]
    mock_connect.return_value = conn

    res = pg.run_query('SELECT 1;')

    assert res == [{'id': 1, 'name': 'a'}]
    conn.close.assert_called_once()


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_run_query_closes_connection_on_exception(mock_connect):
    conn, cur = make_conn_cursor_mocks()
    mock_connect.return_value = conn
    cur.execute.side_effect = RuntimeError('boom')

    with pytest.raises(RuntimeError):
        pg.run_query('SELECT 1;')

    conn.close.assert_called_once()


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_view_exists_closes_connection(mock_connect):
    conn, cur = make_conn_cursor_mocks()
    cur.fetchone.return_value = [True]
    mock_connect.return_value = conn

    assert pg.view_exists('some_view') is True
    conn.close.assert_called_once()


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_add_view_autocommit_ok_and_closes(mock_connect):
    conn, cur = make_conn_cursor_mocks()
    cur.fetchone.return_value = [False]  # for view_exists -> not exists
    # When add_view runs, it will call view_exists again after creation; set True then
    def fetchone_sequence():
        # first call: view_exists before add -> False
        # second call after creation: view_exists after add -> True
        yield [False]
        yield [True]
    fetch_gen = fetchone_sequence()

    def fetchone_side_effect():
        return next(fetch_gen)

    # Route fetchone based on which query executes
    cur.fetchone.side_effect = fetchone_side_effect

    mock_connect.return_value = conn

    # Mock SQL file contents used by add_view
    m = mock_open(read_data="CREATE VIEW v AS SELECT 1;")
    with patch('builtins.open', m):
        assert pg.add_view('some_view') is True
    # Commit may be attempted (harmless with autocommit)
    assert conn.close.called


@patch('services.dataverse.postgresql.psycopg2.connect')
def test_no_idle_in_transaction_simulated(mock_connect):
    """Simulate a long statement that would otherwise hold transaction; our autocommit should prevent idle-in-transaction state.
    We can't inspect pg_stat_activity here, but we can assert that commit/rollback aren't required and connection still closes.
    """
    conn, cur = make_conn_cursor_mocks()
    mock_connect.return_value = conn

    # Simulate a long-running query by making fetchone return multiple rows
    cur.description = [('x',)]
    cur.fetchone.side_effect = [(1,), (2,), (3,), None]

    res = pg.run_query('SELECT generate_series(1,3);')

    assert res == [{'x': 1}, {'x': 2}, {'x': 3}]
    # No explicit rollback/commit required; connection closed
    conn.close.assert_called_once()
