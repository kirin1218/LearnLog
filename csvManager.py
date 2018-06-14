#-*- coding:utf-8 -*-
import sys
import os
import codecs
import json

   
class csvManager:
    def __init__(self,path):
        self._path = path
        self._raw = None
        self._rows = []
        self._size = 0
        self.open()
    
    def parse(self):
        i = 0
        length = len(self._raw)
        cells = []
        stkbuf = '' 
        dquat = False
        while True:
            data = self._raw[i]
           
            if dquat == True:
                if data == '\"':
                    # ファイルの終端
                    if i + 1 >= length:
                        cells.append(stkbuf)
                        stkbuf=''
                    #ダブルクォートの終端
                    elif self._raw[i+1] == ',': 
                        cells.append(stkbuf)
                        stkbuf = ''
                        dquat = False
                        i+=1
                    #ダブルクオートのエスケープ　まだ途中
                    elif self._raw[i+1] == '\"':
                        stkbuf += data
                        i += 1
                    #謎のダブルクォート
                    else:
                        stkbuf + data
                else:
                    stkbuf += data
                i+=1
                
                if i >= length:
                    if len(stkbuf) > 0:
                        cells.append(stkbuf)
                    if len(cells) > 0:
                        self._rows.append(cells)
                    break
            else:
                if len(stkbuf) == 0:
                    if data == '\"':
                        if not i + 1 >= length:
                            if self._raw[i+1] == '\"':
                                if i + 2 >= length and self._raw[i+2] == '\"':
                                    dquat = True
                                else:
                                    stkbuf += data
                                    i+=1
                            else:
                                dquat = True
                            i+=1
                            continue
                if (data == '\r' and self._raw[i+1] == '\n') or data == '\n':
                    cells.append(stkbuf)
                    stkbuf=''
                    self._rows.append(cells)
                    cells = []
                    if data == '\r' and self._raw[i+1] == '\n':
                        i+=1 
                elif data == ',':
                    cells.append(stkbuf)
                    stkbuf=''
                else:
                    stkbuf += data
                i+=1
                if i >= length:
                    if len(stkbuf) > 0:
                        cells.append(stkbuf)
                    if len(cells) > 0:
                        self._rows.append(cells)
                    break
        return len(self._rows)
    
    def open(self):
        self._size = os.path.getsize(self._path)
        with codecs.open(self._path,"rb",'Shift_jis') as f:
            f.seek(0)
            self._raw = f.read()
            self.parse()

    def tojson(self):
        jsondata = {}
        logs =[]
        for log in self._rows:
            logdata = {}
            for i in range(len(log)):
                cell = log[i]
                #print(str(cell,'utf-8'))
                test = cell.encode('utf-8').decode('utf-8')
                print(cell.encode('utf-8'))
                logdata[i] = cell
            logs.append(logdata)
        jsondata['logdata'] = logs
        return jsondata



if __name__ == '__main__':
    path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    csv = csvManager(path)
    jsonpath = '.' + os.sep + 'Data' + os.sep + 'log.json'
    jsondata = csv.tojson()
    with codecs.open(jsonpath,"w",encoding='utf-8') as f:
        json.dump(jsondata, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        #json.dump(jsondata,f,ensure_ascii=False)
    
    with codecs.open(jsonpath,'r',encoding='utf-8') as f2:
        jdata = json.load(f2)
       