import json

def config(num):
    """
    config.jsonを読み出して、設定dictを出力する。
    :param num: 0:普通の設定, 1:学習パラメータ
    :return: 設定dict
    """
    jsonfile = open('config.json', 'r')
    configs = json.load(jsonfile)
    return configs[num]