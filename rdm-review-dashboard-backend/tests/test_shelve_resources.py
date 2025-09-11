from unittest.mock import MagicMock, patch
import services.issue as issue
import services.locks as locks
import services.note as note


@patch('services.issue.shelve')
def test_issue_get_closes_shelve(mock_shelve):
    mock_db = MagicMock()
    mock_db.__iter__.return_value = iter([])
    mock_shelve.open.return_value = mock_db
    res = issue.get('doi:10.1/abc')
    assert isinstance(res, dict)
    mock_db.close.assert_called_once()


@patch('services.locks.shelve')
def test_locks_update_closes_shelve(mock_shelve):
    mock_db = MagicMock()
    mock_shelve.open.return_value = mock_db
    result = locks.update('ds1', 'publishing', True)
    assert result is True
    assert mock_db.close.called


@patch('services.note.shelve')
def test_note_upsert_closes_shelve(mock_shelve, monkeypatch):
    from models.note import Note

    class DummyNote(Note):
        pass

    mock_db = MagicMock()
    mock_shelve.open.return_value = mock_db

    monkeypatch.setattr(note.filesystem, 'BASE_DIR', ['/tmp'])
    monkeypatch.setattr(note.filesystem, 'get_foldername_from_persistent_id', lambda x: 'ds')
    monkeypatch.setattr(note, 'open_note', lambda path, retries=5, waittime_in_s=5: mock_db)

    note.upsert_note('doi:10/abc', 'hello', '@u', 'feedback', note_id='n1')
    assert mock_db.close.called
