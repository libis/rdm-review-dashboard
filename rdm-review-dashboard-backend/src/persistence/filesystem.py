import os
from typing import List
from pathlib import Path
from utils.logging import logging
BASE_DIR = []

def get_foldername_from_persistent_id(persistent_id :str) -> str:
    return persistent_id.replace('doi:', '').replace('/', '_')
    

def make_dir_if_not_exists(file_path:List[str]):
    '''Makes a new dir under the base path, if the new path does not exist. Returns a list of the new dirs made.'''
    base_dir = BASE_DIR.copy()
    new_dirs_made = []
    for folder in file_path:
        if not folder in os.listdir(os.path.join(*base_dir)):
            logging.info(f'Folder not found: Making new folder {folder}')
            os.mkdir(os.path.join(*base_dir, folder ))
            new_dirs_made.append(os.path.join(*base_dir, folder ))
        base_dir.append(folder)
    return new_dirs_made

def file_exists(file_path: List[str]):
    return Path(os.path.join(*file_path)).absolute().exists()