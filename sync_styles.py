from configuration import config
import requests
import json
import logging
import oauth_token

logger = logging.getLogger(__name__)


@oauth_token.api_call(200)
def sync_styles(css_file_path, title, external_reference_code):
    headers = {
        "Accept": "application/json",
        "Authorization": oauth_token.authorization,
        "Content-Type": "application/json",
    }

    DEFAULT_LANGUAGE_ID = "en-US"

    with open(css_file_path) as f:
        styles_file_lines = f.readlines()
    styles_file_content = styles_file_lines[0]

    structured_content_request_body = {
        "availableLanguages": [DEFAULT_LANGUAGE_ID],
        "contentFields": [
            {
                "contentFieldValue": {"data": f"<style>{styles_file_content}</style>"},
                "name": "content",
            },
        ],
        "externalReferenceCode": external_reference_code,
        "contentStructureId": config["BASIC_WEB_CONTENT_STRUCTURE_ID"],
        "title": title,
    }

    session = requests.Session()

    logger.debug(
        f"Created request body {json.dumps(structured_content_request_body, indent=4)}"
    )
    uri = f"{config['OAUTH_HOST']}/o/headless-delivery/v1.0/sites/{config['SITE_ID']}/structured-contents/by-external-reference-code/{external_reference_code}"

    res = session.put(
        uri, headers=headers, data=json.dumps(structured_content_request_body)
    )

    return res


styles_file_name = "main.min.css"

article = sync_styles(
    f"styles/{styles_file_name}", styles_file_name, styles_file_name
).json()
