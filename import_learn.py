import requests
import json
import os
import config
import oauth_token
import import_file
import import_article

config = config.getConfig()

print ("Using host " + config['OAUTH_HOST'])

authorization = oauth_token.getOAUTHToken(config)

session = requests.Session()


def importImages():
	for root,d_names,f_names in os.walk(config['SPHINX_OUTPUT_DIRECTORY']):
		if root.endswith("_images"):
			for f in f_names:
				filename = os.path.join(root, f)
				print("Importing... " + filename)
				import_file.importFile(filename, "commerce_" + f, config,authorization)

importImages()

def importArticles():
	for root,d_names,f_names in os.walk(config['SPHINX_OUTPUT_DIRECTORY']):
		for f in f_names:
			if f.endswith(".fjson"):
				filename = os.path.join(root, f)
				print("Importing... " + filename)
				import_article.importArticle(filename, config, authorization)

importArticles()