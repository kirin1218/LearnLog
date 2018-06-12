#-*- coding:utf-8 -*-
import sys
import os

class csvManager:
    def __init__(self,path):
        self._path = path
        self._raw = None
        self._rows = []
        self.open()
    
    def getline(self,start,linedata,maxidx):
        nextline = start+1
        i = start
        while i <= maxidx:
            data = self._raw[i]
            if data == (b'\r')[0] or data == (b'\n')[0]:
                i+=1
                break
            linedata.append(data)
            i+=1
        nextline = i
        return nextline

    
    def open(self):
        #size = os.path.getsize(self._path)
        with open(self._path,"rb") as f:
            f.seek(0)
            self._raw = f.read()
            size = len(self._raw)
            i = 0
            while i < size:
                linedata = []
                i = self.getline(i,linedata,size-1)

if __name__ == '__main__':
    path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    csv = csvManager(path)


    