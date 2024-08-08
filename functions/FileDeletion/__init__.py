# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import os
from datetime import datetime, timezone
from itertools import islice
import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from shared_code.status_log import State, StatusClassification, StatusLog

def main(mytimer: func.TimerRequest) -> None:
    '''This function is a cron job that runs every 10 miuntes, detects when 
    a file has been deleted in the upload container and 
        1. removes the generated Blob chunks from the content container, 
        2. removes the CosmosDB tags entry, and
        3. updates the CosmosDB logging entry to the Delete state
    If a file has already gone through this process, updates to the code in
    shared_code/status_log.py prevent the status from being continually updated'''
    utc_timestamp = datetime.utcnow().replace(
        tzinfo=timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
