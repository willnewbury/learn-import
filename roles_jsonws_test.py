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
import urllib

@oauth_token.api_call(200)
def get_role():
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/role/get-role"

    logger.info(f"Using uri {uri}")
    method = "GET"

    params = {
        "roleId": 20103,
    }

    res = session.request(method, uri, headers=headers, params=params)

    response_payload = res.json()
    if "error" in response_payload:
        raise Exception(
            "Error invoking get-role: " + response_payload["error"]["message"]
        )

    logger.info(f"Response: {json.dumps(res.json(), indent=4)}")
    return res

# @oauth_token.api_call(200)
# def add_role():
#     logger = logging.getLogger(__name__)
#     session = requests.Session()
#     headers = {
#         "Accept": "application/json",
#         "Authorization": oauth_token.authorization,
#         "Content-Type": "application/json",
#     }
#
#     uri = f"{config['OAUTH_HOST']}/api/jsonws/role/add-role"
#
#     logger.info(f"Using uri {uri}")
#     method = "POST"
#
#     data = {
#         "className": "com.liferay.portal.kernel.model.Role",
#         "classPK": "0",
#         "name": "Jsonws_Test_Role",
#         "titleMap" : "{}",
#         "description" : "{}",
#         "type" : "1",
#         "subtype" : ""
#     }
#
#     res = session.request(method, uri, params=data, headers=headers)
#
#     response_payload = res.json()
#     if "error" in response_payload:
#         raise Exception(
#             "Error invoking add-role: " + response_payload["error"]["message"]
#         )
#
#     logger.info(f"Response: {json.dumps(res.json(), indent=4)}")
#     return res

@oauth_token.api_call(200)
def add_role2():
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/role"

    logger.info(f"Using uri {uri}")
    method = "POST"

    data = {
        "method": "add-role",
        "params": {
            "className": "com.liferay.portal.kernel.model.Role",
            "classPK": 0,
            "name": "Jsonws_Test_Role",
            "titleMap" : json.dumps({'en-US'),
            "description" : "{}",
            "type" : 1,
            "subtype": ""
        },
        "id": 123,
        "jsonrpc": "2.0"
    }

    logger.info(f"Executing {json.dumps(data, indent=4)}")
    logger.info(f"Executing {method}")
    res = session.request(method, uri, headers=headers, data=json.dumps(data))

    response_payload = res.json()
    if "error" in response_payload:
        raise Exception(
            "Error invoking add-role: " + response_payload["error"]["message"]
        )

    logger.info(f"Response: {json.dumps(res.json(), indent=4)}")
    return res

#get_role()
#add_role()
add_role2()