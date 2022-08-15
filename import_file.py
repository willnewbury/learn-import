import requests
import json
import config
import oauth_token
import mimetypes

def importFile(filepath, filename, config, authorization):
	headers = {
		"Authorization": authorization
	}

	session = requests.Session()
	post_uri = f"{config['OAUTH_HOST']}/o/headless-delivery/v1.0/sites/{config['SITE_ID']}/documents"

	image_type = mimetypes.guess_type(filepath)
	mime_type = image_type[0]
	if mime_type is None:
		raise Exception ("cannot figure out mimetype for" + filepath)

	res = session.post(post_uri, headers=headers,
		files=(
			('document', (None, json.dumps({"title": filename, "externalReferenceCode": filename}))),
			('file', (filename, open(filepath, 'rb'), str(mime_type)),
		)))
	print (res.text)