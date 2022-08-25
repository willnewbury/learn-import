from configuration import config
from decorators import timer
from util import save_as_json, sha_256sum
import get_articles
import get_documents
from document_folder import (
    add_missing_document_folders,
    get_liferay_document_folders_by_path,
)
import import_article
import import_document
import json
import logging
import os
import requests
import traceback


logger = logging.getLogger(__name__)

LEARN_ARTICLE_JSON_EXTENSION = ".fjson"

session = requests.Session()


@timer
def collect_sphinx_files():
    articles_by_article_key = {}
    document_paths = set()
    images = []
    other = []
    for root, d_names, f_names in os.walk(config["SPHINX_OUTPUT_DIRECTORY"]):
        for f in f_names:
            filename = str(os.path.join(root, f))
            # Sample path - /home/allenz/liferay/liferay-learn/site/build/output/commerce/latest/en/search.fjson
            # Get the sphinx relevant part of the path into sphinx_output_path, i.e. commerce/latest/en/search.fjson
            _, sphinx_output_path = filename.split(config["SPHINX_OUTPUT_DIRECTORY"])

            if sphinx_output_path.startswith("homepage"):
                (product, *subdirectories, name) = sphinx_output_path.split(os.sep)
                version = "latest"
                language = "en"
            else:
                (
                    product,
                    version,
                    language,
                    *subdirectories,
                    name,
                ) = sphinx_output_path.split(os.sep)

            if filename.endswith(LEARN_ARTICLE_JSON_EXTENSION):
                article_key = f"{product}_{version}_{'_'.join(subdirectories)}_{name}"

                translation = {
                    "language": language,
                    "filename": filename,
                    "image_prefix": f"{product}_{version}_{language}__images_",
                }
                if article_key not in articles_by_article_key:
                    articles_by_article_key[article_key] = {
                        "product": product,
                        "translations": [translation],
                    }
                else:
                    articles_by_article_key[article_key]["translations"].append(
                        translation
                    )
            elif root.endswith("_images"):
                images.append(
                    {
                        "filename": filename,
                        "import_filename": f"{product}_{version}_{language}_{'_'.join(subdirectories)}_{name}",
                        "path": "",
                        "product": product,
                        "version": version,
                        "language": language,
                        "sha_256sum": sha_256sum(filename),
                    }
                )
            elif filename.endswith(".zip"):
                path = "/".join([product, version, language] + subdirectories)
                document_paths.add(path)
                images.append(
                    {
                        "filename": filename,
                        "import_filename": "name",
                        "path": path,
                        "product": product,
                        "version": version,
                        "language": language,
                        "sha_256sum": sha_256sum(filename),
                    }
                )
            else:
                other.append(filename)

    articles = []
    for article_by_article_key in articles_by_article_key:
        articles.append(
            {
                "article_key": article_by_article_key,
                **articles_by_article_key[article_by_article_key],
            }
        )

    save_as_json("articles_by_article_key", articles_by_article_key)
    save_as_json("articles", articles)
    save_as_json("images", images)
    save_as_json("other", other)
    save_as_json("document_paths", sorted(document_paths))

    return [articles, images, other, sorted(document_paths)]


@timer
def import_images(documents_by_title, images):
    file_counter = 0
    for image in images:
        import_document.import_document(
            image["filename"],
            image["import_filename"],
            documents_by_title,
            image["sha_256sum"],
        )

        file_counter = file_counter + 1
        if (
            config["IMAGE_IMPORT_LIMIT"] > 0
            and file_counter >= config["IMAGE_IMPORT_LIMIT"]
        ):
            logger.warning(
                f"Stopping import due to import limit being reached {config['IMAGE_IMPORT_LIMIT']}!"
            )
            break
    logger.info(f"Imported {file_counter} files")


@timer
def import_articles(articles, articles_by_friendlyurlpath):
    article_counter = 0
    for article in articles:
        import_article.import_article(article, articles_by_friendlyurlpath)

        article_counter = article_counter + 1
        if (
            config["ARTICLE_IMPORT_LIMIT"] > 0
            and article_counter >= config["ARTICLE_IMPORT_LIMIT"]
        ):
            logger.warning(
                f"Stopping article import due to import limit being reached {config['ARTICLE_IMPORT_LIMIT']}"
            )
            break

    logger.info(f"Imported {article_counter} articles.")


@timer
def import_learn():
    import_success = False

    try:
        sphinx_articles, images, other, sphinx_document_paths = collect_sphinx_files()
        liferay_document_folders_by_path = get_liferay_document_folders_by_path()
        add_missing_document_folders(
            sphinx_document_paths, liferay_document_folders_by_path
        )
        documents_by_title = get_documents.get_documents()
        import_images(documents_by_title, images)
        articles_by_friendlyurlpath = get_articles.get_articles()
        import_articles(sphinx_articles, articles_by_friendlyurlpath)

        import_success = True
    except BaseException as err:
        logger.error(f"Unexpected {err=}, {type(err)=}, {traceback.format_exc()}")

    logger.info(
        f"Learn import was {'successful' if import_success else 'NOT successful'}."
    )


import_learn()
