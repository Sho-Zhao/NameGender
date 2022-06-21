import json

def config():
    jsonfile = open('config.json', 'r')
    configs = json.load(jsonfile)
    return configs[0]