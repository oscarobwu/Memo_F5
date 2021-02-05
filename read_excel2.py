#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       read_excel2.py
#
#        USAGE: read_excel2.py
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
#      Created Time: 2021-01-05 13:31:21
#      Last modified: 2021-01-05 15:44
#     REVISION: ---
#===============================================================================
import pandas as pd
#Insert complete path to the excel file and index of the worksheet
df = pd.read_excel("2021-01-05-15-01_vs_pool.xlsx", sheet_name='10.100.0.22')
# insert the name of the column as a string in brackets
list1 = list(df['vs_name'])
list2 = list(df['Pool_memb'])
#
VIP_inupt = input('VS_Name : ')
#df1 = df[['vs_ip_addr', 'vs_ip_port', 'vs_pool']]
#print(list1)
#print(list2)
#print(df1)
for x,y in zip(list1, list2):
	#print("vs : {} poolmember: {}".format(x, y))
	#g = y.split('\n')
	#print("poolmember: {}".format( y))
	if x == VIP_inupt:
		g = y.split()
		for t in g:
			print("pool_member: {} ".format(t))
