#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       test_color.py
#
#        USAGE: test_color.py
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
#      Created Time: 2021-01-05 18:44:34
#      Last modified: 2021-01-05 18:55
#     REVISION: ---
#===============================================================================
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file with a
# conditional formatting using Pandas and XlsxWriter.
#
# Copyright 2013-2020, John McNamara, jmcnamara@cpan.org
#

import pandas as pd


# Create a Pandas dataframe from some data.
#df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})
df = pd.read_excel('2021-01-05-18-22_vs_pool.xlsx', sheet_name='Sheet1')
#df = df1[['vs_ip_addr', 'vs_ip_port', 'vs_pool']]
#df = df1[['vs_ip_addr']]

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_conditional.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Apply a conditional format to the cell range.
worksheet.conditional_format('C2:C38', {'type': '3_color_scale'})

# Close the Pandas Excel writer and output the Excel file.
writer.save()
