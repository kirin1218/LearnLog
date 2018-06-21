#-*- coding:utf-8 -*-
import json
import codecs
import os
import dictionary as dic
import const
import re
class sepJson:
    const.NO_DATA = 0
    const.FILE_PATH_UNKNOWN = 0
    const.FILE_PATH_NORMAL = 1
    const.FILE_PATH_UNC =2

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
                
    def parseFilepath(self,i_path):
        pos = i_path.rfind('\\')
        o_file = i_path[pos+1:]
        o_dir = i_path[:pos+1]
        pos = o_file.rfind('.')
        o_ext = o_file[pos+1:]
        if len(o_dir) < 2:
            o_type = const.FILE_PATH_UNKNOWN
            o_root = 'UNKNOWN'
            print(i_path)
        elif o_dir[0] == '\\' and o_dir[1] == '\\':
            o_type = const.FILE_PATH_UNC
            npos = o_dir[2:].find('\\')
            o_root =  o_dir[2:npos+2]
        elif o_dir[1] == ':' and o_dir[2] == '\\':
            o_type = const.FILE_PATH_NORMAL
            o_root = o_dir[0]
        else:
            o_type = const.FILE_PATH_UNKNOWN
            o_root = 'UNKNOWN'
        return o_type,o_dir,o_file,o_ext,o_root 

    def parseWindowNameArea(self, wndname_area, extention):
        pos = wndname_area.find('size<')
        if pos != -1:
            epos = wndname_area.find('>')
            if epos != -1:
                filesize_str = wndname_area[pos+5:epos]
                extention['file_size'] = filesize_str
                wndname_area = wndname_area[:pos] + wndname_area[epos+1:]

        pos = wndname_area.find('l<')
        if pos != -1:
            epos = wndname_area.find('>')
            if epos != -1:
                filearea = wndname_area[pos+2:epos]
                parsearea = filearea.split(' ')
                parsesize = len(parsearea)
                if parsesize == 1:
                    extention['file_area'] = parsearea[0]
                elif parsesize == 2:
                    extention['dest_area'] = parsearea[1]
                elif parsesize == 3:
                    extention['src_area'] = parsearea[0]
                    extention['dest_area'] = parsearea[2]

                wndname_area = wndname_area[:pos] + wndname_area[epos+1:]
        return wndname_area
        
    def parseOpeName(self,ope,extention):
        s1 = ope.split('<')
        #SePインストール<Version 3.6.42.1>の<以降は不要なためいったん削除（使う時がきたら考える）
        if len(s1) > 1:
            print('delete a part of opename,{0},delstring:<{1}'.format( ope, s1[1]))
            ope = s1[0]
            ver = s1[1].split('>')[0]
            extention['sepinst_ver'] = ver

        #拒否-印刷やファイル書き込み(DeP)-警告パネルなどちょくちょく出てくる
        if ope.startswith('拒否-') == True:
            extention['ope_flag_deny'] = True
            ope = ope[3:]

        if ope.endswith('-警告パネル') == True:
            extention['ope_flag_depalert'] = True
            ope = ope[:-6]

        #編集履歴の-途中
        if ope.endswith('-途中') == True:
            extention['ope_flag_editlogprogress'] = True
            ope = ope[:-3]

        if ope.endswith('(プロセス)') == True:
            extention['ope_flag_editlog_process'] = True
            ope = ope[:-6]

        if ope.endswith('(ペースト)') == True:
            extention['ope_flag_editlog_paste'] = True
            ope = ope[:-6]

        if ope.endswith('(ファイル)') == True:
            extention['ope_flag_editlog_file'] = True
            ope = ope[:-6]

        if ope.endswith('(インターネット)') == True:
            extention['ope_flag_editlog_internet'] = True
            ope = ope[:-9]


        #Write制限
        if ope.endswith('(SV-Write制限)') == True or ope.endswith('(sv-write制限)') == True:
            extention['ope_flag_writelimit'] = True
            ope = ope[:-12]

        #SV暗号化
        if ope.endswith('(SV-暗号)') == True or ope.endswith('(sv-暗号)') == True:
            extention['ope_flag_svenc'] = True
            ope = ope[:-7]

        if ope.endswith('(SV-リリース承認IN)') == True or ope.endswith('(sv-リリース承認in)') == True:
            extention['ope_flag_rel_approval_in'] = True
            ope = ope[:-13]
        elif ope.endswith('(SV-リリース承認Zip OUT)') == True or ope.endswith('(sv-リリース承認zip out)') == True:
            extention['ope_flag_rel_approval_zipout'] = True
            ope = ope[:-18]
        elif ope.endswith('(SV-リリース承認平文OUT)') == True or ope.endswith('(sv-リリース承認平文out)') == True:
            extention['ope_flag_rel_approval_plainout'] = True
            ope = ope[:-16]

        if ope.endswith('(信頼ストレージ暗号領域)') == True: 
            extention['ope_flag_storageenc_area'] = True
            ope = ope[:-13]

        if ope.endswith('(DeP)') == True or ope.endswith('(dep)') == True:
            extention['ope_flag_dep'] = True
            ope = ope[:-5]

        if ope.endswith('(Web)') == True or ope.endswith('(web)') == True:
            extention['ope_flag_web'] = True
            ope = ope[:-5]

        if ope.endswith('(アップロード)') == True:
            extention['ope_flag_upload'] = True
            ope = ope[:-8]
        elif ope.endswith('(ダウンロード)') == True:
            extention['ope_flag_download'] = True
            ope = ope[:-8]

        s2 = ope.split('-')
        if len(s2) > 1:
            print(ope)

        s2 = ope.split('(')
        if len(s2) > 1:
            print(ope)
        return ope

    def parseExtention(self,raw):
        extention = {}
        #まずは操作名
        ope = self.parseOpeName(raw['6'],extention)
        
        if ope == 'ファイルコピー':
            src_file = raw['2']
            src_dir = raw['3']
            pathtype,fdir,fname,ext,root = self.parseFilepath(src_dir+src_file)
            extention['src_dir'] = fdir
            extention['src_file'] = fname
            extention['src_ext'] = ext
            extention['src_root'] = root
            extention['src_type'] = pathtype

            dest_path = raw['9']
            pathtype,fdir,fname,ext,root = self.parseFilepath(dest_path)
            extention['dest_dir'] = fdir
            extention['dest_file'] = fname
            extention['dest_ext'] = ext
            extention['dest_root'] = root
            extention['dest_type'] = pathtype

            #ウィンドウ名の列を分解する
            extention['window_title'] = self.parseWindowNameArea(raw['5'],extention)
            
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

        extention = sepjson['extention']
        if 'src_file' in extention:
            logdic['src_file'] = self._dict.dictionalize('FileName',extention['src_file'])
        if 'src_ext' in extention:
            logdic['src_ext'] = self._dict.dictionalize('FileExt',extention['src_ext'])
        if 'src_area' in extention:
            logdic['src_area'] = self._dict.dictionalize('PathArea',extention['src_area'])
        if 'src_file' in extention:
            logdic['dest_file'] = self._dict.dictionalize('FileName',extention['dest_file'])
        if 'dest_ext' in extention:
            logdic['dest_ext'] = self._dict.dictionalize('FileExt',extention['dest_ext'])
        if 'dest_area' in extention:
            logdic['dest_area'] = self._dict.dictionalize('PathArea',extention['dest_area'])
        if 'window_title' in extention:
            logdic['window_title'] = self._dict.dictionalize('window_title',extention['window_title'])


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

 