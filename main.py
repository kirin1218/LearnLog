#-*- coding:utf-8 -*-
import sys
import os
import numpy as np
import csvManager as csv
import json
import codecs
import sepJson as sj

def outputJson(data,path):
    with codecs.open(jsonpath,"w",encoding='utf-8') as f:
        #json.dump(jsondata, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        json.dump(jsondata, f, ensure_ascii=False)

if __name__ == '__main__':
    #path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    path = 'z:\SePLog\henmi_20180611.csv'
    csv = csv.csvManager(path)
    #読み込んだCSVをJson形式に変換
    jsondata = csv.tojson(name='logdata')
    #Jsonファイルとして出力
    jsonpath = 'z:\SePLog\log.json'
    #jsonpath = '.' + os.sep + 'Data' + os.sep + 'log.json'
    outputJson(jsondata,jsonpath)
    #SeP/DeP履歴としてjsonファイルを読み込む
    sepjson = sj.sepJson(raw=jsonpath)