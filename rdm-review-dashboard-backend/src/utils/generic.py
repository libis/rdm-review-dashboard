from enum import Enum
import json 

def read_json(fn):
    with open(fn, 'r') as fp:     
        j = json.load(fp)
    return j

def write_json(fn, dictionary):
    with open(fn, 'w') as fp:     
        j = json.dump(dictionary, fp)
    return

def enum_from_dict(name, dictionary):
    return Enum(name, dictionary)

def convert_bytes_to_gb(bytes: int) -> float:
    '''convert given byte to GBs'''
    return bytes / 1000 ** 3

def id_from_args(* args):
    return '_'.join([str(arg) for arg in args]).replace('doi:', '').replace('/', '').replace(':', '').replace(' ', '').replace('.', '').replace('%2F', '').replace('-', '')

async def async_id_from_args(* args):
    return '_'.join([str(arg) for arg in args]).replace('doi:', '').replace('/', '').replace(':', '').replace(' ', '').replace('.', '').replace('%2F', '').replace('-', '')

async def get_persistent_id(doi: str, identifier:str)->str:
    if not doi.startswith('doi:'):
        doi = 'doi:' + doi
    return f"{doi}/{identifier}"
