from enum import Enum
import json 
from pathlib import Path
from utils.logging import logging

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

def read_value_from_file(file_path, required=False):
    file = Path(file_path).absolute()
    if not file.exists():
        if required:
            logging.info(f"{file_path} file not found.")
            raise FileNotFoundError
        return None
    with open(file) as f:
        return f.readline().strip()
    
async def async_get_authority_and_identifier(persistent_identifier: str):
    authority = persistent_identifier.split("/")[0].replace("doi:", "")
    identifier = "/".join(persistent_identifier.split("/")[1:])
    return authority, identifier
