from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

import utils.request_utils as rq


@patch('utils.request_utils.httpx.AsyncClient')
def test_async_get_uses_timeout(mock_client_cls):
    mock_client = MagicMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = False
    mock_client.get = AsyncMock(return_value=MagicMock(status_code=200))
    mock_client_cls.return_value = mock_client

    asyncio.run(rq.async_get_request('http://x'))
    # Client constructed with timeout
    assert 'timeout' in mock_client_cls.call_args.kwargs
    # Call also passes timeout
    assert 'timeout' in mock_client.get.call_args.kwargs


@patch('utils.request_utils.requests.get')
def test_sync_get_uses_timeout(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    rq.get_request('http://x')
    assert 'timeout' in mock_get.call_args.kwargs


@patch('utils.request_utils.httpx.AsyncClient')
def test_async_post_uses_timeout(mock_client_cls):
    mock_client = MagicMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = False
    mock_client.post = AsyncMock(return_value=MagicMock(status_code=200))
    mock_client_cls.return_value = mock_client

    asyncio.run(rq.async_post_request('http://x', key=None))
    assert 'timeout' in mock_client_cls.call_args.kwargs
    assert 'timeout' in mock_client.post.call_args.kwargs


@patch('utils.request_utils.requests.post')
def test_sync_post_uses_timeout(mock_post):
    mock_post.return_value = MagicMock(status_code=200)
    rq.post_request('http://x', key=None)
    assert 'timeout' in mock_post.call_args.kwargs


@patch('utils.request_utils.requests.delete')
def test_delete_uses_timeout(mock_delete):
    mock_delete.return_value = MagicMock(status_code=200)
    rq.delete_request('http://x')
    assert 'timeout' in mock_delete.call_args.kwargs
