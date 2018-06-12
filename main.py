#-*- coding:utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd
import csvManager as csv

if __name__ == '__main__':
    path = '.' + os.sep + 'Data' + os.sep + 'log.csv'
    csv = csv.csvManager(path)

   #csv_input = pd.read_csv(filepath_or_buffer=path,encoding='utf-8',sep=',')
    #print(type(csv_input))
