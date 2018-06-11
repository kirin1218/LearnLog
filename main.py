#-*- coding:utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd

if __name__ == '__main__':
    path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    size = os.path.getsize(path)
    with open(path,"rb") as f:
        f.seek(0)
        data = f.read(size)
    print(data)
    #csv_input = pd.read_csv(filepath_or_buffer=path,encoding='utf-8',sep=',')
    #print(type(csv_input))
