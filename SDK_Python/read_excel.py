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
#      Created Time: 2021-02-02 12:52:05
#      Last modified: 2021-02-02 16:03
#     REVISION: ---
#===============================================================================
import pandas as pd
File_Name = input('File_name: ')  #要处理的文件路径
df = pd.read_excel(File_Name, sheet_name=None)
print(df)
#drop_row = input('row : ')
#aaa = df.drop([ drop_row ])
#print( aaa)
