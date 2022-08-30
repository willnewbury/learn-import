from configuration import config
from decorators import timer
import json
import logging
import logging.config
import mimetypes
import os
import oauth_token
import requests
import sys


@timer
@oauth_token.api_call(200)
def get_file_entry_types_invoke(group_ids):
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/invoke"

    logger.debug(f"Using uri {uri}")
    method = "GET"
    cmd = {"/dlfileentrytype/get-file-entry-types": {"groupIds": group_ids}}

    logger.info(f"Executing {json.dumps(cmd, indent=4)}")
    res = session.request(method, uri, headers=headers, data=json.dumps(cmd))
    logger.info(f"Response: {res.content}")
    return res


@timer
@oauth_token.api_call(200)
def get_file_entry_types(group_ids):
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/dlfileentrytype/get-file-entry-types"

    logger.debug(f"Using uri {uri}")
    method = "GET"
    cmd = {"/dlfileentrytype/get-file-entry-types": {"groupIds": group_ids}}

    logger.info(f"Executing {json.dumps(cmd, indent=4)}")
    res = session.request(method, uri, headers=headers, params={"groupIds": group_ids})
    logger.info(f"Response: {json.dumps(res.json(), indent=4)}")
    return res


@timer
@oauth_token.api_call(200)
def add_file_entry_type(data_definition_id, name):
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/dlfileentrytype"

    logger.debug(f"Using uri {uri}")
    method = "POST"

    data = {
        "method": "add-file-entry-type",
        "params": {
            "groupId": int(config["SITE_ID"]),
            "dataDefinitionId": int(data_definition_id),
            "fileEntryTypeKey": "",
            "nameMap": {"en-US": name},
            "descriptionMap": {"en-US": name},
        },
        "id": 123,
        "jsonrpc": "2.0",
    }

    logger.info(f"Executing {json.dumps(data, indent=4)}")
    res = session.request(method, uri, headers=headers, data=json.dumps(data))
    logger.info(f"Response: {json.dumps(res.json(), indent=4)}")
    return res


@timer
@oauth_token.api_call(200)
def add_file_entry_type_invoke(data_definition_id, name):
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/invoke"

    logger.debug(f"Using uri {uri}")
    method = "POST"

    data = {
        "/dlfileentrytype/add-file-entry-type": {
            "groupId": int(config["SITE_ID"]),
            "dataDefinitionId": int(data_definition_id),
            "fileEntryTypeKey": "",
            "nameMap": {"en-US": name},
            "descriptionMap": {"en-US": name},
        },
    }

    logger.debug(f"Executing {json.dumps(data, indent=4)}")
    res = session.request(method, uri, headers=headers, data=json.dumps(data))
    logger.debug(f"Response: {json.dumps(res.json(), indent=4)}")
    return res
