from services.dataverse import solr
from services.dataverse import native
from services import note
import json
from typing import List, Optional, Tuple, Literal
from enum import Enum
from services.dataverse import user
from utils.generic import async_id_from_args, async_get_authority_and_identifier
from utils.logging import logging
import asyncio
from services.dataverse import postgresql


class ReviewStatus(Enum):
    DRAFT = 'draft'
    SUBMITTED_FOR_REVIEW = 'submitted_for_review'
    IN_REVIEW = 'in_review'
    DEACCESSIONED = 'deaccessioned'
    PUBLISHED = 'published'



async def format_version_number(majorVersion: Optional[int]=None, minorVersion: Optional[int]=None)-> float:
    """Formats major and minor version numbers into 1 decimal place."""
    minorVersion = minorVersion or 0
    majorVersion = majorVersion or 0
    return float(str(majorVersion) +  "." + str(minorVersion))



async def get_dataset_storage_usage():
    """
    Retrieves dataset sizes from SOLR index.
    Returns:
        dict: {
                "persisntentIdDataset1": fileSizeInBytes,
                ...
                }

    
    """
    res = await solr.async_retrieve_dataset_sizes()
    file_sizes = {}
    if res.status_code == 200:
        resp = json.loads(res.text)
        file_sizes_list = resp.get('facet_counts', {}).get('facet_pivot', {}).get('parentIdentifier', [])
        for file_size_record in file_sizes_list:
            file_sizes[file_size_record['value']] = file_size_record.get('stats', {}).get('stats_fields', {}).get('fileSizeInBytes', {}).get('sum', 0)
    return file_sizes



async def format_dataset_metadata(record):
    async def format_status(row):
        status = row.get('versionstate').lower()
        reviewers = row.get('reviewer')
        if status == 'released':
            status = 'published'
        locks_ =  row.get('locks')
        if locks_ and 'InReview' in locks_:
            status = 'in_review' if reviewers else 'submitted_for_review'
        return ReviewStatus(status)
    metadata = record.pop('metadata')
    version_major_number = record.pop('versionnumber')
    version_minor_number = record.pop('minorversionnumber')
    record["identifier"] = f"doi:{record.pop('authority')}/{record.pop('identifier')}"
    record["reviewer"] = [reviewer.strip('@') for reviewer in record.pop('reviewers') or []]
    record["lastUpdateTime"] = record.pop('lastupdatetime')
    version_num = await format_version_number(version_major_number, version_minor_number)
    if version_num == 0:
        version_num = None
    record['versionMinorNumber'] = version_minor_number
    record['versionMajorNumber'] = version_major_number
    record['version'] = version_num
    record['title'] = metadata.get('title', [None])[0]
    record['description'] = metadata.get('dsDescriptionValue', [None])[0]
    record['authorName'] = metadata.get('authorName',  list())
    record['status'] = await format_status(record)
    record['department'], record['faculty'] = await differentiate_departments_faculties(metadata.get('departmentFaculty'))
    return record

async def append_dataset_storage_usage(datasets):
    file_sizes = await get_dataset_storage_usage()
    for i, record in enumerate(datasets):
        datasets[i]['size'] = file_sizes.get(record['identifier'])
    return datasets

async def async_get_dataset_details(persistent_identifier: str):
    """
    Queries a dataset's metadata from postgresql.

    Args:
        persistent_identifier (str): Persistent identifier of the dataset
    
    """
    authority, identifier = await async_get_authority_and_identifier(persistent_identifier)
    records = postgresql.query_dataset_metadata(authority, identifier)
    result = []
    for record in records:
        new_record = await format_dataset_metadata(record)
        result.append(new_record)
    result = await append_dataset_storage_usage(result)

    return result[0] if len(result)>0 else None
    
async def sanitize_reviewer_username(reviewer):
    if reviewer and not reviewer.startswith('@'):
        reviewer = "@" + reviewer
    return reviewer

async def async_get_dataset_draft_metadata(persistent_identifier):
    res = await native.async_retrieve_dataset_draft_details(persistent_identifier)
    result = None
    if res.status_code == 200:
        result = json.loads(res.text)
    return result


async def async_get_datasets_details(start=None, rows=False, status=None, reviewer=None):
    """
    Queries all datasets' metadata from postgresql. 
    
    Args:
        status (Optional str): filter datasets by status.
        reviewer (Optional str): filter datasets by reviewer assignment.

        start (Optional int): starting row.
        rows (Optional int): number of rows retrieved.
    """

    reviewer = await sanitize_reviewer_username(reviewer)
    records = postgresql.query_datasets_metadata(start=start, rows=rows, status=status, reviewer=reviewer)
    result = []
    for record in records:
        new_record = await format_dataset_metadata(record)
        result.append(new_record)
    result = await append_dataset_storage_usage(result)

    return result


async def get_dataset_status(persistent_identifier: str) -> ReviewStatus:
    '''Retrieves the status of the latest version of the dataset'''
    dataset = await async_get_dataset_details(persistent_identifier)
    if dataset and dataset.get('status'):
        return ReviewStatus(dataset.get('status'))
    else:
        return None

async def change_status(persistent_identifier: str, to_status:Literal['draft', 'in_review', 'deaccessioned', 'published', 'returned_to_author'], version:Optional[Literal['minor', 'major', 'updatecurrent']]=None, reason:Optional[str]=None, user_id: Optional[str]=None):
    from_status = await get_dataset_status(persistent_identifier)
    to_status = ReviewStatus(to_status)
    dataverse_response = None
    feedback = None
    if from_status == ReviewStatus.DRAFT and to_status == ReviewStatus.IN_REVIEW:
        dataverse_response = await native.submit_for_review(persistent_identifier)

    elif to_status == ReviewStatus.PUBLISHED:
        dataverse_response = await native.publish(persistent_identifier, version)

    elif from_status == ReviewStatus.IN_REVIEW and to_status == ReviewStatus.DRAFT:
        note_id = await async_id_from_args(persistent_identifier)
        feedback = note.get_note_by_id(persistent_identifier, note_id, 'feedback')
        dataverse_response = await native.return_to_author(persistent_identifier, feedback.get('text'))

    return dataverse_response

async def differentiate_departments_faculties(department_faculty: Optional[List[str]]) -> Tuple[List[str], List[str]]:
    department_faculty = department_faculty or []
    faculties = []
    departments = []
    for item in department_faculty:
        if not isinstance(item, str):
            continue
        if 'faculty' in item.lower():
            faculties.append(item.strip())
        elif 'department' in item.lower():
            departments.append(item.strip())
    return departments, faculties

async def get_review_status_counts(reviewer=None):
    if reviewer and not reviewer.startswith('@'):
        reviewer = "@" + reviewer
    records = postgresql.query_dataset_review_status_counts(reviewer=reviewer)
    result = {
        'in_review': {'status': 'in_review', 'count': 0},
        'draft': {'status': 'draft', 'count': 0},
        'submitted_for_review': {'status': 'submitted_for_review', 'count': 0},
        'published': {'status': 'published', 'count': 0}
    }
    for row in records:
        dataset_count = row.get('datasetcount')
        if row.get('versionstate')=='RELEASED':
            result['published']['count'] = result.get('published').get('count') + dataset_count
        elif row.get('versionstate')=='DRAFT' and row.get('inreview') == True:
            if row.get('hasreviewer') == True:
                result['in_review']['count'] = result.get('in_review').get('count') + dataset_count
            else:
                result['submitted_for_review']['count'] = result.get('submitted_for_review').get('count') + dataset_count
        elif row.get('versionstate')=='DRAFT' and row.get('inreview') == False:
            result['draft']['count'] = result.get('draft').get('count') + dataset_count
    result['all'] = {'status': 'all', 'count': sum([c.get('count') for c in result.values()])}
    return result

async def get_dataset_contact(persistent_identifier):

    response = await native.async_retrieve_dataset_details(persistent_identifier)
    if response.status_code != 200:
        return logging.error(f"{response.status_code}, {response.text}")
    citation_blocks = json.loads(response.text).get("data", {}).get("latestVersion", {}).get("metadataBlocks", {}).get("citation", {}).get("fields", [])
    dataset_contact_block = None
    for field in citation_blocks:
        if field.get("typeName") == "datasetContact":
            dataset_contact_block = field.get("value")
            break
    contacts = []
    if dataset_contact_block:
        for value in dataset_contact_block:
            contacts.append(
                {
                    "datasetContactName": value.get("datasetContactName", {}).get("value"),
                    "datasetContactAffiliation": value.get("datasetContactAffiliation", {}).get("value"),
                    "datasetContactEmail": value.get("datasetContactEmail", {}).get("value"),
                }
            )
            
    return contacts