import json
from data_definition_rest import post_site_data_definition_by_content_type
from document_type import add_file_entry_type_invoke

with open("site-setup/learn_article.json", encoding="utf-8") as f:
    data_definition = json.load(f)
    data_definition = post_site_data_definition_by_content_type(
        "journal", data_definition
    ).json()


with open("site-setup/learn_synced_file.json", encoding="utf-8") as f:
    data_definition = json.load(f)
    data_definition = post_site_data_definition_by_content_type(
        "document-library", data_definition
    ).json()

    add_file_entry_type_invoke(data_definition["id"], "Learn Synced File")
