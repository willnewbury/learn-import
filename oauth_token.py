import requests
import json

from requests import auth

def getOAUTHToken(config):
	post_uri = config['OAUTH_HOST'] + '/o/oauth2/token'
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	session = requests.Session()
	res = session.post(post_uri, headers=headers,
		data={
				"client_id": config["CLIENT_ID"],
				"client_secret": config["CLIENT_SECRET"],
				"grant_type": "client_credentials"
			}
		)
	token_payload = res.json()
	authorization = token_payload["token_type"] + " " + token_payload["access_token"]
	session.headers.update({"Authorization": authorization})
	print(json.dumps(res.json(), indent=4))
	return authorization


