import requests
import httpx 
from utils.logging import logging 

DEFAULT_TIMEOUT = 30  # seconds

async def async_get_request(request_url, key=None, headers=None, verify= None, **kwargs):
    params = {}
    verify = verify or False
    headers = headers or {}
    if key:
        params = dict(key=key)
    if kwargs:
        params.update(kwargs)
    logging.info(f'async get request: {request_url}')
    async with httpx.AsyncClient(verify=verify, timeout=DEFAULT_TIMEOUT) as client:
        res = await client.get(request_url, params=params, timeout=DEFAULT_TIMEOUT)
        logging.info(f'response {request_url, res.status_code}')
        if res.status_code != 200:
            logging.info(res.text)
        return res

def get_request(request_url, key=None, headers=None, verify= None, **kwargs):
    params = {}
    verify = verify or False
    headers = headers or {}
    if key:
        params = dict(key=key)
        if '?' not in request_url:
            request_url += f'?key={key}'
        else:
            request_url += f'&key={key}'
    if kwargs:
        params.update(kwargs)
    logging.info(f'sync get request: {request_url}')
    res = requests.get(request_url, params=params, verify=verify, timeout=DEFAULT_TIMEOUT)
    logging.info(f'response {request_url, res.status_code}')
    if res.status_code != 200:
        logging.info(res.text)
    return res

async def async_post_request(request_url, key, headers=None, data=None, json_dict=None, verify=None, **kwargs):
    data = data or {}
    headers = headers or {}
    json_dict = json_dict or {}
    verify = verify or False
    request_url_params = []
    if key:
        kwargs.update({'key':key})
    if kwargs:
        for k, v in kwargs.items():
            request_url_params.append(f'{k}={v}') 
        request_url = f'{request_url}?{"&".join(request_url_params)}'
    logging.info(f'async post request: {request_url}')
    async with httpx.AsyncClient(verify=verify, timeout=DEFAULT_TIMEOUT) as client:
        res = await client.post(request_url, data=data, headers=headers, json=json_dict, timeout=DEFAULT_TIMEOUT)
        logging.info(f'response {request_url, res.status_code}')
        if res.status_code != 200:
            logging.info(res.text)
    return res


def post_request(request_url, key, headers=None, data=None, json_dict=None, verify=None, **kwargs):
    data = data or {}
    headers = headers or {}
    json_dict = json_dict or {}
    verify = verify or False
    request_url_params = []
    if key:
        kwargs.update({'key':key})
    if kwargs:
        for k, v in kwargs.items():
            request_url_params.append(f'{k}={v}') 
        request_url = f'{request_url}?{"&".join(request_url_params)}'
    logging.info(f'sync post request: {request_url}')
    res = requests.post(request_url, data=data, json=json_dict, headers=headers, verify=verify, timeout=DEFAULT_TIMEOUT)
    logging.info(f'response {request_url, res.status_code}')
    if res.status_code != 200:
        logging.info(res.text)
    return res

def delete_request(request_url, key=None, headers=None, verify=None):
    verify = verify or False
    headers = headers or {}
    if key:
        if '?' not in request_url:
            request_url = f'{request_url}?key={key}'
        else:
            request_url = f'{request_url}&key={key}'
    logging.info(f'sync delete request: {request_url}')
    res = requests.delete(request_url, verify=verify, timeout=DEFAULT_TIMEOUT)
    logging.info(f'response {request_url, res.status_code}')
    if res.status_code != 200:
        logging.info(res.text)

    return res