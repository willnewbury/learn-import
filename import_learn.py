import configuration
import get_articles
import import_article
import import_file
import oauth_token
import os
import requests

LEARN_ARTICLE_JSON_EXTENSION = ".fjson"

config = configuration.getConfig()

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

#importImages()
#articles = get_articles.getArticles(config, authorization)
#print(json.dumps(articles, indent=4))


def importArticles():
	for root,d_names,f_names in os.walk(config['SPHINX_OUTPUT_DIRECTORY']):
		for f in f_names:
			if f.endswith(LEARN_ARTICLE_JSON_EXTENSION):
				filename = os.path.join(root, f)
				print("Importing... " + filename)
				import_article.importArticle(filename, config, authorization)

importArticles()