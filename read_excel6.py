#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       read_excel6.py
#
#        USAGE: read_excel6.py
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
#      Created Time: 2021-01-08 16:15:50
#      Last modified: 2021-01-08 16:17
#     REVISION: ---
#===============================================================================
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import xlrd

#First part of the code, used only to create some Excel file with data

wbk = xlsxwriter.Workbook('hello.xlsx')
wks = wbk.add_worksheet()
i = -1

for x in range(1, 1000, 11):
    i+=1
    cella = xl_rowcol_to_cell(i, 0) #0,0 is A1!
    cellb = xl_rowcol_to_cell(i, 1)
    cellc = xl_rowcol_to_cell(i, 2)
    #print (cella)
    wks.write(cella,x)
    wks.write(cellb,x*3)
    wks.write(cellc,x*4.5)
#myPath= r'C:\Desktop\hello.xlsx'
myPath= 'hello.xlsx'
wbk.close()

#SecondPart of the code

for sh in xlrd.open_workbook(myPath).sheets():
    for row in range(sh.nrows):
        for col in range(sh.ncols):
            myCell = sh.cell(row, col)
            print(myCell)
            if myCell.value == 300.0:
                print('-----------')
                print('Found!')
                print(xl_rowcol_to_cell(row,col))
                quit()
