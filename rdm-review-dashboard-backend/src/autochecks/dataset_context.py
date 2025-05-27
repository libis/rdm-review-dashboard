from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel
from utils.logging import logging
from services.dataverse import native
import json 
        



class DatasetContext:
    persistent_id : str
    metadata_blocks : dict|None = None
    metadata : dict
    dataset_metadata_json : dict
    files : list

    def get_metadata(self, persistent_id: str) -> dict:
        response = native.retrieve_dataset_details(persistent_id)
        if response.status_code == 200:
            return json.loads(response.text).get("data")
        else:
            raise Exception(f"Could not retrieve dataset metadata for {persistent_id}: \n" + response.text)

    def __init__(self, persistent_id: str):
        self.persistent_id = persistent_id
        dataset = {}
        try:
            dataset = self.get_metadata(persistent_id)
        except Exception as e:
            logging.error(f"Could not retrieve metadata for dataset {persistent_id}")
            logging.error(e)
        if not dataset:
            raise Exception(f"Could not load dataset metadata for {persistent_id}")
        self.dataset_metadata_json = dataset
        
        self.metadata_blocks = dataset["latestVersion"] \
            .get("metadataBlocks")
        if self.metadata_blocks:
            # print(self.metadata_blocks)
            try:
                self.metadata = self.parse_metadata_blocks(self.metadata_blocks)
            except Exception as e:
                logging.error(f"Could not flatten metadata for dataset {persistent_id}")
                raise
        else:
            raise Exception("Could not retrieve dataset info.")
        self.files = dataset.get("latestVersion", {}) \
            .get("files")

    def parse_metadata_blocks(self, metadata: dict) -> dict:
        result = {}
        for blockname, block in metadata.items():
            block_result = {}
            for field in block.get("fields"):
                block_result.update(self.parse_block(field))
            result[blockname] = block_result
        return result

    def parse_block(self, block:dict)->dict: # type: ignore
        typeName = block["typeName"]
        typeClass = block["typeClass"]
        multiple = block["multiple"]
        value = block["value"]
        if typeClass=="primitive" or typeClass=="controlledVocabulary":
            return {typeName: value}

        if multiple and typeClass == "compound":
            multipleValue = []
            for subblock in value:
                subblockValue = {}
                for compoundBlockField in subblock.values():
                    subblockValue.update(self.parse_block(compoundBlockField))
                multipleValue.append(subblockValue)
            return {typeName: multipleValue}
        elif (not multiple) and typeClass == "compound":
            compoundValue = {}
            for compoundBlock in value.values():
                compoundValue.update(self.parse_block(compoundBlock))
            return {typeName: compoundValue}
            
        
