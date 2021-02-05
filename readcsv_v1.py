#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       readcsv.py
#
#        USAGE: readcsv.py
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
#      Created Time: 2021-01-21 13:47:59
#      Last modified: 2021-01-22 08:28
#     REVISION: ---
#===============================================================================
import csv
import sys
#
#Checlip = input('IPaddress: ')
print('請輸入資料_IP_Address，直接按下Enter 結束 : ')
buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        buffer.append(line)
#print (buffer)
member_list = buffer

print('開始執行 ############################## ')
#
with open("protagonist.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for lines in csv_reader:
        #result.append(record.split('-')[0])
        pmaddr = lines['Pool_Members']
        pmname = lines['Pool_Name']
        pmaddrsp = pmaddr.split(';')
        #pmaddrsp1 = [i.split('|')[1] for i in pmaddrsp]
        for i in pmaddrsp:
            try:
                pamaddrsp1 = i.split('|')[1]
                pamaddrsp0 = i.split('|')[0]
                if pamaddrsp1 in member_list:
                    print("poolName :{} poomMember :{} poolMemberaddr: {}".format(pmname, pamaddrsp0, pamaddrsp1))
            except:
                continue

#print("{} {}".format(pmname, pmaddrsp1))
#        for pmaddrsp1 in pmaddrsp:
#            print(pmaddrsp1.split('|')[1])
#        #print(lines['Partition'], lines['Pool_Members'])
