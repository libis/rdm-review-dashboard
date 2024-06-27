from utils import request_utils


BASE_URL = ''
KEY = None

async def async_retrieve_datasets(start=None, rows=None):
    request_url=f"{BASE_URL}/collection1/select?indent=true&q.op=OR&q=dvObjectType%3Adatasets"
    if start:
        request_url += f"&start={start}"

    if rows:
        request_url += f"&rows={rows}"

    result = await request_utils.async_get_request(request_url=request_url, key=KEY)
    return result

async def async_retrieve_dataset(identifier: str):
    request_url=f"{BASE_URL}/collection1/select?indent=true&q.op=AND&q=dvObjectType:datasets+identifier:{identifier}"
    result = await request_utils.async_get_request(request_url=request_url, key=KEY)
    return result


def retrieve_datasets(start=None, rows=None):
    request_url=f"{BASE_URL}/collection1/select?indent=true&q.op=OR&q=dvObjectType%3Adatasets"
    if start:
        request_url += f"&start={start}"

    if rows:
        request_url += f"&rows={rows}"

    result = request_utils.get_request(request_url=request_url, key=KEY)
    return result

def retrieve_dataset_sizes():
    request_url = f"{BASE_URL}/collection1/select?facet.pivot={{!stats=piv}}parentIdentifier&facet=true&indent=true&q.op=AND&q=dvObjectType%3Afiles&rows=0&stats.field={{!tag=piv sum=true}}fileSizeInBytes&stats=true"
    result = request_utils.get_request(request_url=request_url, key=KEY)
    return result

async def async_retrieve_dataset_sizes():
    request_url = f"{BASE_URL}/collection1/select?facet.pivot={{!stats=piv}}parentIdentifier&facet=true&indent=true&q.op=AND&q=dvObjectType%3Afiles&rows=0&stats.field={{!tag=piv sum=true}}fileSizeInBytes&stats=true"
    result = await request_utils.async_get_request(request_url=request_url, key=KEY)
    return result