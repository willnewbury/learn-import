import json
import logging
import requests


def getOAUTHToken(config):
    logger = logging.getLogger(__name__)

    post_uri = config["OAUTH_HOST"] + "/o/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    session = requests.Session()
    res = session.post(
        post_uri,
        headers=headers,
        data={
            "client_id": config["CLIENT_ID"],
            "client_secret": config["CLIENT_SECRET"],
            "grant_type": "client_credentials",
        },
    )

    if not res.status_code == 200:
        errorMessage = "Failed to get oauth token" + json.dumps(res.json(), indent=4)
        logger.error(errorMessage)
        raise Exception(errorMessage)

    logger.info("Received OAuth token")
    token_payload = res.json()
    authorization = token_payload["token_type"] + " " + token_payload["access_token"]

    return authorization
