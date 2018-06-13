#-*- coding:utf-8 -*-
import sys
import os
def char(charactor):
    ret =  charactor[0]
    print(ret,type(ret))
    return ret
    
class csvManager:
    def __init__(self,path):
        self._path = path
        self._raw = None
        self._rows = []
        self.open()
    
    def getline(self,start,linedata,maxidx):
        nextline = start+1
        CR = char(b'\r')
        LF = char(b'\n')
        COMMA = char(b',')
        i = start
        cells = []
        stkbuf = '' 
        while i <= maxidx:
            data = self._raw[i]
            if data == CR or data == LF:
                cells.append(str(stkbuf))
                stkbuf=''
                while self._raw[i] == CR or self._raw[i] == LF:
                    i+=1 
                continue
            elif data == COMMA:
                cells.append(stkbuf.decode('shift-jis'))
                stkbuf=''
            else:
                stkbuf += chr(data)
            i+=1
        nextline = i
        return nextline

    
    def open(self):
        #size = os.path.getsize(self._path)
u        with open(self._path,"rb",'Shift_jis') as f:
            f.seek(0)
            self._raw = f.read()
            print(self._raw)
            size = len(self._raw)
            i = 0
            while i < size:
                linedata = []
                i = self.getline(i,linedata,size-1)

if __name__ == '__main__':
    path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    csv = csvManager(path)


    