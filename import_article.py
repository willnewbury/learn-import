import requests
import json
import hashlib


def getBreadcrumbElement(parent):
    link = parent["link"]
    title = parent["title"]
    return f'<a href="{link}">{title}</a>'


def getBreadcrumb(current_page_name, parents):
    breadcrumbs = map(getBreadcrumbElement, parents)
    return " &nbsp; / &nbsp;".join(breadcrumbs)


def importArticle(filepath, config, authorization):
    headers = {
        "Accept": "application/json",
        "Authorization": authorization,
        "Content-Type": "application/json",
    }

    with open(filepath, encoding="utf-8") as f:
        article_data = json.load(f)

    if not "body" in article_data:
        print("No HTML body found for " + filepath)
        return

    if not "parents" in article_data:
        article_data["parents"] = []

    if not "display_toc" in article_data:
        article_data["display_toc"] = False

    if not "navtoc" in article_data:
        article_data["navtoc"] = ""

    externalReferenceCode = hashlib.sha256(
        article_data["current_page_name"].encode()
    ).hexdigest()

    article = {
        "contentFields": [
            {
                "contentFieldValue": {
                    "data": article_data["body"].replace(
                        "../../_images/",
                        "/webdav/learn-python-import/document_library/commerce_",
                    )
                },
                "name": "Body",
            },
            {
                "contentFieldValue": {
                    "data": getBreadcrumb(
                        article_data["current_page_name"], article_data["parents"]
                    )
                },
                "name": "Breadcrumb",
            },
            {
                "contentFieldValue": {
                    "data": article_data["toc"] if article_data["display_toc"] else ""
                },
                "name": "TOC",
            },
            {
                "contentFieldValue": {"data": article_data["navtoc"]},
                "name": "Navigation",
            },
        ],
        "contentStructureId": config["ARTICLE_STRUCTURE_ID"],
        "externalReferenceCode": externalReferenceCode,
        "friendlyUrlPath": article_data["current_page_name"] + ".html",
        "title": article_data["title"],
    }

    session = requests.Session()

    uri = f"{config['OAUTH_HOST']}/o/headless-delivery/v1.0/sites/{config['SITE_ID']}/structured-contents/by-external-reference-code/{externalReferenceCode}"
    # post_uri = f"{config['OAUTH_HOST']}/o/headless-delivery/v1.0/sites/{config['SITE_ID']}/structured-contents"

    res = session.put(uri, headers=headers, data=json.dumps(article))
