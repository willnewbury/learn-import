from configuration import config
from document_folder_rest import post_document_folder, get_document_folder_batch
import get_all_items
import json
import logging
import oauth_token
import requests
import util


def add_missing_document_folders(
    sphinx_document_paths, liferay_document_folders_by_path
):
    """Check all paths in sphinx_document_paths to see if they exist on the server (stored in liferay_document_folders_by_path) and create any missing folders."""
    _logger = logging.getLogger(__name__)
    for sphinx_document_path in sphinx_document_paths:
        if sphinx_document_path not in liferay_document_folders_by_path:
            _logger.info(f"Adding folders for {sphinx_document_path}")
            add_missing_document_folders_for_sphinx_document_path(
                liferay_document_folders_by_path, sphinx_document_path
            )


def add_missing_document_folders_for_sphinx_document_path(
    liferay_document_folders_by_path, sphinx_document_path
):
    """Check all the component path parts for a single path (sphinx_document_path) and add any missing folders"""
    _logger = logging.getLogger(__name__)
    sphinx_document_path_components = sphinx_document_path.split("/")

    parentDocumentFolderId = 0

    document_path_prefix = ""
    for sphinx_document_path_component in sphinx_document_path_components:
        document_path = document_path_prefix + sphinx_document_path_component

        _logger.debug(f"Checking document path {document_path}")

        if document_path not in liferay_document_folders_by_path:
            new_liferay_document_folder = post_document_folder(
                sphinx_document_path_component, parentDocumentFolderId
            ).json()

            liferay_document_folders_by_path[document_path] = {
                "id": new_liferay_document_folder["id"],
                "parentDocumentFolderId": parentDocumentFolderId,
            }

            parentDocumentFolderId = new_liferay_document_folder["id"]
        else:
            parentDocumentFolderId = liferay_document_folders_by_path[document_path][
                "id"
            ]

        document_path_prefix = document_path + "/"


def get_path(liferay_document_folders, liferay_document_folder, path):
    """Calculate paths for list of document folders on the Liferay server"""
    logger = logging.getLogger(__name__)
    logger.debug(f"get_path for {liferay_document_folder['name']} and path {path}")

    next_path = (
        liferay_document_folder["name"] + "/" + path
        if path
        else liferay_document_folder["name"]
    )

    if "parentDocumentFolderId" in liferay_document_folder:
        return get_path(
            liferay_document_folders,
            next(
                filter(
                    lambda document_folder: document_folder["id"]
                    == liferay_document_folder["parentDocumentFolderId"],
                    liferay_document_folders,
                )
            ),
            next_path,
        )
    else:
        return next_path


def get_liferay_document_folders_by_path():
    """Prepare a list of document folders found on the Liferay server indexed by path"""
    logger = logging.getLogger(__name__)

    liferay_document_folders = get_all_items.get_all_items(get_document_folder_batch)

    liferay_document_folders_by_path = {}

    for liferay_document_folder in liferay_document_folders:
        liferay_document_folders_by_path[
            get_path(liferay_document_folders, liferay_document_folder, "")
        ] = liferay_document_folder

    util.save_as_json("liferay_document_folders", liferay_document_folders)
    util.save_as_json(
        "liferay_document_folders_by_path", liferay_document_folders_by_path
    )
    return liferay_document_folders_by_path
