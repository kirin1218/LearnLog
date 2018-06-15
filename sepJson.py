#-*- coding:utf-8 -*-
import json
import codecs
import os

class sepJson:
    def __init__(self,path=None,raw=None):
        self._path = path
        self._data = None
        if self._path is None:
            if raw is not None:
                with codecs.open(raw,'r',encoding='utf-8') as f:
                    rawdata = json.load(f)
                    self.convert(rawdata)
    #csvから変換されただけのjsonファイルを解析用の形式に変換する
    def convert(self,rawdata):
        print('a')
'''
    def isloadedraw(self):
        if self._rawdata is not None:
            return True
        return False
    def printRaw(self):
        if self.isloadedraw() != False:
            print(json.dumps(self._rawdata,ensure_ascii=False))
        else:
            print('don\'t loaded raw file')
'''
if __name__ == '__main__':
    jsonpath = '.' + os.sep + 'Data' + os.sep + 'log.json'
    sepjson = sepJson(raw=jsonpath)
 