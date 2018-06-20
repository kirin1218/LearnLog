#-*- coding:utf-8 -*-
import json
import codecs
import os
import dictionary as dic
import const
import re

class sepJson:
    const.NO_DATA = 0
    def __init__(self,path=None,raw=None):
        self._path = path
        self._dict = dic.Dictionary()
        if self._path is None:
            self._logs = []
            self._data = {}
            self._data['logs'] = self._logs
            self._data['dictionary'] = None
            if raw is not None:
                with codecs.open(raw,'r',encoding='utf-8') as f:
                    rawdata = json.load(f)
                    self.convert(rawdata)
        else:
            with codecs.open(self._path,'r',encoding='utf-8') as f:
                self._data = json.load(f)
                self._logs = self._data['logs'] 
                self._dict.set(self._data['dictionary']) 

    def combine(self,words,connect):
        ret = ''
        for word in words:
            if ret != '':
                ret += connect
            ret+=word
        return ret
                
    def parseExtention(self,raw):
        extention = {}
        #まずは操作名
        ope = raw['6']
        s1 = ope.split('<')
        #SePインストール<Version 3.6.42.1>の<以降は不要なためいったん削除（使う時がきたら考える）
        if len(s1) > 1:
            print('delete a part of opename,{0},delstring:<{1}'.format( ope, s1[1]))
            ope = s1[0]
            ver = s1[1].split('>')[0]
            extention['sepinst_ver'] = ver

        #拒否-印刷やファイル書き込み(DeP)-警告パネルなどちょくちょく出てくる
        s2 = ope.split('-')
        if len(s2) > 1:
            #まずは先頭についているパターンを判定
            if s2[0] == '拒否':
                extention['ope_flag_deny'] = True
                #print('detect deny flag{0}'.format(ope))
                s2.pop(0)
                ope = self.combine(s2,'-')

        #文字列を数値化（辞書の作成）する
        #jopeno = self._dict.dictionalize(name='OpeName',data=ope)
        return ope,extention

    def parseLogdata(self,raw):
        common = {}
        extention = None 
        common['PCName'] = raw['1']
        common['AppName'] = raw['4']
        common['UserName'] = raw['7']
        common['date'] = raw['8']    
        common['OpeName'],extention = self.parseExtention(raw)

        return common,extention

    def dictionalize(self,sepjson):
        logdic = {}
        #まずは操作名
        cmn = sepjson['common']
        logdic['OpeName'] = self._dict.dictionalize('OpeName',cmn['OpeName'])

        return logdic

    #csvから変換されただけのjsonファイルを解析用の形式に変換する
    def convert(self,rawdata):
        lines = rawdata['logdata']
        for line in lines:
            size = len(self._logs)
            if size%100000 == 0:
                print('{0}\'s line convert'.format(size))
            raw = {}
            sepjson = {}
            #0:PC名
            raw['1'] = line['0']
            #1:ファイル名
            raw['2'] = line['1']
            #2:フォルダパス
            raw['3'] = line['2']
            #3:アプリ名
            raw['4'] = line['3']
            #4:ウィンドウ名
            raw['5'] = line['4']
            #5:操作名
            raw['6'] = line['5']
            #6:ユーザー名
            raw['7'] = line['6']
            #7:日時
            raw['8'] = line['7']    
            #8:その他情報
            raw['9'] = line['8']   
            
            sepjson['raw'] = raw
            sepjson['common'],sepjson['extention'] = self.parseLogdata(raw)
            sepjson['dictionary'] = self.dictionalize(sepjson)
            '''
            #9:そのほか情報の初期化
            sepjson['ope_flag_deny'] = False
            sepjson['ope_flag_deplog'] = False
            sepjson['ope_flag_depalertpanel']  = False
            sepjson['ope_flag_depdetect']  = False
            sepjson['OpeName_Dict'] = const.NO_DATA
            '''
            self._logs.append(sepjson)
        
    def dump(self,path):
        #辞書データを書き込みデータに代入する
        self._data['dictionary'] = self._dict.get()
        with codecs.open(path,"w",encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            #json.dump(jsondata,f,ensure_ascii=False)
        #こっちを参照しないように初期化しておく
        self._data['dictionary'] = None

     def filterFromDic(self,ItemName,ItemData,include=True):
        newJson = sepJson()
        first = True
        dictval = const.NO_DATA
        dictName = ''
        for log in self._logs:
            if first != False:
                #辞書化したキーが存在するか
                if ItemName in log['dictionary']:
                    dictval = self._dict.getValue(ItemName,ItemData)
                    if dictval == const.NO_DATA:
                        print('Exist dictionary Key:{0},but not exist value'.format(dictName))
                        return None
                first = False
            if log['dictionary'][ItemName] == dictval: 
                if include == True:
                    newJson._logs.append(log)
            else:
                if include == False:
                    newJson._logs.append(log)
        if newJson.size() == 0:
            print('filter not found match data,ItemName:{0},ItemData:{1}'.format(ItemName,ItemData))
            return None
        newJson._dict = self._dict
        return newJson
    def filter(self,ItemName,ItemData,include=True):
        newJson = sepJson()
        first = True
        dictval = const.NO_DATA
        dictName = ''
        for log in self._logs:
            if first != False:
                #検索対象のキーが存在するか
                if not ItemName in log:
                    print('sepjson not found item \'{0}\''.format(ItemName))
                    return None
                #辞書化したキーが存在するか
                if ItemName in log['dictionary']:
                    dictval = self._dict.getValue(ItemName,ItemData)
                    if dictval == const.NO_DATA:
                        print('Exist dictionary Key:{0},but not exist value'.format(dictName))
                        return None
                first = False
            if dictval != const.NO_DATA:
                if log['dictionary'][ItemName] == dictval: 
                    if include == True:
                        newJson._logs.append(log)
                else:
                    if include == False:
                        newJson._logs.append(log)
            else:
                srchRet = re.search(ItemData,log[ItemName])
                if not srchRet is None:
                    if include == True:
                        newJson._logs.append(log)
                else:
                    if include == False:
                        newJson._logs.append(log)
        if newJson.size() == 0:
            print('filter not found match data,ItemName:{0},ItemData:{1}'.format(ItemName,ItemData))
            return None
        newJson._dict = self._dict
        return newJson

    def size(self):
        return len(self._logs)
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
    hhmode = True
    read_seplog_json = True
    
    if hhmode == True:
        jsonpath = 'z:\SePLog\log.json'
        logjsonpath = 'z:\SePLog\seplog.json'
    else:
    jsonpath = '.' + os.sep + 'Data' + os.sep + 'log.json'
        logjsonpath = '.' + os.sep + 'Data' + os.sep + 'seplog.json'

    if read_seplog_json == False:
    sepjson = sepJson(raw=jsonpath)
    sepjson.dump(logjsonpath) 
    else:
        sepjson = sepJson(path=logjsonpath)

    filecopylog = sepjson.filterFromDic(ItemName='OpeName',ItemData='ファイルコピー',include=True)
    #filecopylog = sepjson.filter(ItemName='AppName',ItemData='svchost',include=True)

 