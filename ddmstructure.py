from configuration import config
from decorators import timer
import json
import logging
import logging.config
import mimetypes
import os
import oauth_token
import requests


@timer
@oauth_token.api_call(200)
def add_ddmstructure():
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/ddm.ddmstructure/add-structure"
    logger.info(f"Using uri {uri}")
    method = "GET"
    params = {
        "groupId": int(config["SITE_ID"]),
        "classNameId": int(123123),
        "nameMap": {"en-US": "hello"},
        "descriptionMap": {"en-US": "hello"},
        "ddmForm": {"name": "test"},
        "ddmFormLayout": {"name": "test"},
        "storageType": "",
    }

    logger.info(f"Executing {json.dumps(params, indent=4)}")
    res = session.request(method, uri, headers=headers, params=params)
    logger.info(f"Response: {res.content}")
    print(res.status_code)


@timer
@oauth_token.api_call(200)
def fetch_classname(className):
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
    cmd = {"/classname/fetch-class-name": {"value": className}}

    logger.debug(f"Executing {json.dumps(cmd, indent=4)}")
    res = session.request(method, uri, headers=headers, data=json.dumps(cmd))
    logger.debug(f"Response: {json.dumps(res.json(), indent=4)}")
    return res


@timer
@oauth_token.api_call(200)
def add_ddmstructure_invoke(classnameid):
    logger = logging.getLogger(__name__)
    session = requests.Session()
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    uri = f"{config['OAUTH_HOST']}/api/jsonws/invoke"

    logger.info(f"Using uri {uri}")
    method = "POST"
    cmd = {
        "/ddm.ddmstructure/add-structure": {
            "groupId": int(config["SITE_ID"]),
            "classNameId": int(classnameid),
            "nameMap": {"en-US": "hello"},
            "descriptionMap": {"en-US": "hello"},
            "ddmForm": {"nameMap": {"en-US": "Learn DDM Form"}},
            "ddmFormLayout": {"name": "test"},
            "storageType": "",
        }
    }

    logger.info(f"Executing {json.dumps(cmd, indent=4)}")
    res = session.request(method, uri, headers=headers, data=json.dumps(cmd))
    logger.info(f"Response: {json.dumps(res.json(), indent=4)}")
    return res


journal_article_classname = fetch_classname(
    "com.liferay.journal.model.JournalArticle"
).json()


# add_ddmstructure_invoke(journal_article_classname["classNameId"])


# add_ddmstructure()
