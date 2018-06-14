#-*- coding:utf-8 -*-
import sys
import os
import codecs

   
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
                        break
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

if __name__ == '__main__':
    path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    csv = csvManager(path)


    