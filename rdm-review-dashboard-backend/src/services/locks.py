from persistence import filesystem
import shelve
import os 
from utils.logging import logging
from services.dataverse.dataset import metadata
import datetime


def update(unit_id, lock_type, new_value):
    logging.info(f"locks update: {unit_id}, {lock_type}, {new_value}")
    file_path = os.path.join(*filesystem.BASE_DIR, 'locks')
    logging.info(f'lockfile path {file_path}')
    locks = None
    try:
        # modified = False
        locks = shelve.open(file_path)
        try:
            unit_locks = locks[unit_id]
        except Exception:
            unit_locks = {}
        if new_value:
            # if new value: update the lock for dataset
            unit_locks[lock_type] = new_value
            # modified = True
        elif unit_locks:
            # if none: del the lock type from dataset
            unit_locks.pop(lock_type, None)
            # modified = True
        if unit_locks:
            # if locks for dataset -> update
            locks[unit_id] = unit_locks
        else:
            # if not -> remove the dataset from the file (ignore if absent)
            try:
                del locks[unit_id]
            except Exception:
                pass
        try:
            locks.update()
        except Exception as e:
            logging.info(e)
            return False
    except Exception as e:
        logging.info(e)
        return False
    finally:
        if locks is not None:
            try:
                locks.close()
            except Exception:
                pass
    return True

def add(dataset_id, lock_type):
    return update(dataset_id, lock_type, datetime.datetime.now())

def remove(dataset_id, lock_type):
    return update(dataset_id, lock_type, None)
    

def get():
    result = {}
    file_path = os.path.join(*filesystem.BASE_DIR, 'locks')

    try:
        locks = shelve.open(file_path, flag='r')
        result = dict(locks)
        locks.close()
    except Exception as e:
        logging.info(e)
        result = {}
    
    return result

async def verify_and_update_locks():
    locks = await metadata.get_all_dataset_locks()
    datasets = await metadata.get_dataset_list()
    published_datasets = set()
    draft_or_in_review_datasets = set()
    for _dataset in datasets:
        if 'Published' in _dataset.get('publicationStatus'):
            published_datasets.add(_dataset.get('identifier'))
        if 'Draft' in _dataset.get('publicationStatus') or 'In Review' in _dataset.get('publicationStatus'):
            draft_or_in_review_datasets.add(_dataset.get('identifier'))
    
    datasets_to_aremove_locks = published_datasets.difference(draft_or_in_review_datasets)
    logging.info(f'remove locks for {datasets_to_aremove_locks}')
    for dataset_id in datasets_to_aremove_locks:
        if 'publishing' in locks.get(dataset_id, []):
            logging.info(f'removing publishing lock for {dataset_id}')
            update(dataset_id, 'publishing', None)
        


