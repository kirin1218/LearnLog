#-*- coding:utf-8 -*-
import os
import const

class logDictonary:
    def __init__(self,dictdata=None):
        if dictdata is None:
            self._dict = {}
        else:
            self._dict = dictdata

    def set(self,dictdata):
        self._dict = dictdata

    def get(self):
        return self._dict
        
    def dictinalize(self, name, data ):
        if not name in self._dict:
            self._dict[name] = {}
            self._dict[name]['names'] = {}
            self._dict[name]['values'] = {}
            #0番目はDummyデータとして欠番にする
            self._dict[name]['names']['NO_DATA'] = 0
            self._dict[name]['values'][0] = 'NO_DATA'

        dict = self._dict[name]
        names = dict['names']
        values = dict['values']

        if not data in names:
            next = len(values) #0番目はDummyデータ
            names[data] = next
            values[next] = data
            return next
        else:
            return names[data]


