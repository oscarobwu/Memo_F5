#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       read_excel.py
#
#        USAGE: read_excel.py
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
#      Created Time: 2021-01-05 13:18:57
#      Last modified: 2021-01-05 13:27
#     REVISION: ---
#===============================================================================
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('2021-01-05-09-42_vs_pool.xlsx', sheet_name='Sheet1')
#
#
df1 = df[['vs_ip_addr', 'vs_ip_port', 'vs_pool', 'Pool_memb']]

print("Column headings:")
print(df.columns)
print(df1)
#sepalWidth = df['Sepal width']
#sepalLength = df['Sepal length']
#petalLength = df['Petal length']
