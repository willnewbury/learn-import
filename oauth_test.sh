#!/bin/bash

echo "This script assumes jq is installed"

function export_json_to_env () {
    INPUT_FILE="${1}"
    while IFS=$'\t\n' read -r LINE; do
        export "${LINE?}"
    done < <(
        <"${INPUT_FILE}" jq \
            --compact-output \
            --raw-output \
            --monochrome-output \
            --from-file \
            <(echo 'to_entries | map("\(.key)=\(.value)") | .[]')
    )
}

export_json_to_env "./config.local.json"

curl -s "${OAUTH_HOST}/o/oauth2/token" -d "client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&grant_type=client_credentials" | jq

# Example of posting a document
#curl -i -H "Authorization: Bearer ${TOKEN}" -F document="{\"title\": \"5.png\",\"contentUrl\":\"/documents/83630/0/02.png\"}" -F file=@/home/allenz/liferay/liferay-learn/site/build/output/commerce/latest/en/_images/05.gif \
#         "${OAUTH_HOST}/o/headless-delivery/v1.0/sites/${SITEID}/documents" --trace-ascii ./out