#-*- coding:utf-8 -*-
import json
import codecs
import os
import logDictonary as ld
import const

class sepJson:
    const.NO_DATA = 0
    def __init__(self,path=None,raw=None):
        self._path = path
        self._dict = ld.logDictonary()
        if self._path is None:
            if raw is not None:
                self._logs = []
                self._dictinary = {}
                self._data = {}
                self._data['logs'] = self._logs
                self._data['dictinary'] = None
                with codecs.open(raw,'r',encoding='utf-8') as f:
                    rawdata = json.load(f)
                    self.convert(rawdata)
        else:
            with codecs.open(self._path,'r',encoding='utf-8') as f:
                self._data = json.load(f)
                self._logs = self._data['logs'] 
                self._dict.set(self._data['dictinary']) 

    def combine(words,connect):
        ret = ''
        for word in words:
            if ret != '':
                ret += connect
            ret+=word
        return ret
    
    
    def dictinalizeOepName(self):
        for log in self._logs:
            ope = log['OpeName']
            s1 = ope.split('<')
            #SePインストール<Version 3.6.42.1>の<以降は不要なためいったん削除（使う時がきたら考える）
            if len(s1) > 1:
                print('delete a part of opename,{0},delstring:<{1}'.format( ope, s1[1]))
                ope = s1[0]
            #拒否-印刷やファイル書き込み(DeP)-警告パネルなどちょくちょく出てくる
            s2 = ope.split('-')
            if len(s2) > 1:
                #まずは先頭についているパターンを判定
                if s2[0] == '拒否':
                    log['ope_flag_deny'] = True
                    print('detect deny flag{0}'.format(ope))
                    s2.pop(0)
                    ope = self.combine(s2,'-')
            #文字列を数値化（辞書の作成）する
            log['ope_no'] = self._dict.dictinalize(name='OpeName',data=ope)

    #csvから変換されただけのjsonファイルを解析用の形式に変換する
    def convert(self,rawdata):
        lines = rawdata['logdata']
        for line in lines:
            sepjson = {}
            #0:PC名
            sepjson['PCName'] = line['0']
            #1:ファイル名
            sepjson['2'] = line['1']
            #2:フォルダパス
            sepjson['3'] = line['2']
            #3:アプリ名
            sepjson['AppName'] = line['3']
            #4:ウィンドウ名
            sepjson['5'] = line['4']
            #5:操作名
            sepjson['OpeName'] = line['5']
            #6:ユーザー名
            sepjson['UserName'] = line['6']
            #7:日時
            sepjson['date'] = line['7']    
            #8:その他情報
            sepjson['9'] = line['8']   
            #9:そのほか情報の初期化
            sepjson['ope_flag_deny'] = False
            sepjson['ope_flag_deplog'] = False
            sepjson['ope_flag_depalertpanel']  = False
            sepjson['ope_flag_depdetect']  = False
            sepjson['ope_no'] = const.NO_DATA
            self._logs.append(sepjson)
        
        self.dictinalizeOepName()
    
    def dump(self,path):
        #辞書データを書き込みデータに代入する
        self._data['dictinary'] = self._dict.get()
        with codecs.open(path,"w",encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            #json.dump(jsondata,f,ensure_ascii=False)
        #こっちを参照しないように初期化しておく
        self._data['dictinary'] = None

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
    #jsonpath = '.' + os.sep + 'Data' + os.sep + 'log.json'
    #sepjson = sepJson(raw=jsonpath)
    logjsonpath = '.' + os.sep + 'Data' + os.sep + 'seplog.json'
    #sepjson.dump(logjsonpath) 
    #sepjson = sepJson(path=logjsonpath)

 