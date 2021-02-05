#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       read_excel3.py
#
#        USAGE: read_excel3.py
#
#  DESCRIPTION: 
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Oscarob Wu(oscarobwu@gmail.com), 
# ORGANIZATION: 
#      VERSION: 1.0
#      Created Time: 2021-01-08 13:09:01
#      Last modified: 2021-01-08 15:58
#     REVISION: ---
#===============================================================================
import pandas as pd
#file = '2021-01-07-18-03_vs_pool.xlsx'
#require_cols = [0]


#df = pd.read_excel(file, sheet_name='10.100.0.22', usecols = require_cols)
#df2 = pd.DataFrame(columns=['Pool_memb'])
#ppp = df2.head()
#print(df2)

#import pandas
#import pandas as pd

#excel_data_df = pandas.read_excel('2021-01-07-18-03_vs_pool.xlsx', sheet_name='10.100.0.22', usecols=['vs_name', 'vs_pool'])
excel_data_df = pd.read_excel('2021-01-07-18-03_vs_pool.xlsx', sheet_name='10.100.0.22', usecols=['vs_name', 'vs_pool', 'Pool_memb'])
print(excel_data_df)

oo = excel_data_df[excel_data_df["vs_name"]=='vs_10.100.4.31_https'].head()
print(oo)
#data = excel_data_df.columns.values[0]
#print (data)

