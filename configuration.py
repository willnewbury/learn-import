import json
import os
from os.path import exists


def getConfig():
    configfile = "./config.json"
    localconfigfile = "./config.local.json"

    if exists(localconfigfile):
        configfile = localconfigfile

    print("Using config file" + configfile)

    with open(configfile, encoding="utf-8") as configfile:
        config = json.load(configfile)

    return config
