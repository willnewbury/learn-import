import requests


def getArticles(config, authorization):
    headers = {
        "Accept": "application/json",
        "Authorization": authorization,
        "Content-Type": "application/json",
    }

    session = requests.Session()

    get_uri = f"{config['OAUTH_HOST']}/o/headless-delivery/v1.0/sites/{config['SITE_ID']}/structured-contents?fields=id,friendlyUrlPath"

    res = session.get(get_uri, headers=headers)

    return res.json()
