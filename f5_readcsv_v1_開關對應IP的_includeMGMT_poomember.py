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
#      Last modified: 2021-01-22 09:06
#     REVISION: ---
#===============================================================================
import csv
import sys
import re
import logging
import getpass
import time
#  Local Application/Library Specific
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import datetime
import sys, getopt
#
#  Get login password from CLI
F5_host = input('F5_Host: ')
f5user = input('Username: ')
f5pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, f5user, f5pw)
#
#  Get list of pools and pool members
pools = mgmt.tm.ltm.pools.get_collection()
FORMAT = '%(asctime)s %(levelname)s %(module)s %(message)s'
logging.basicConfig(format=FORMAT, level='INFO')
logger = logging.getLogger('set_pool_members_state')
#  Node to search for
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
print("選擇開關機的方式?\n")
print("[1] enabled\n")
print("[2] disabled\n")
print("[3] forced_offline\n")
print("[4] checked\n")
Sele = input("Your choice (press enter to skip): ")
if Sele == '1':
    action = 'enabled' # 開啟
elif Sele == '2':
    action = 'disabled' # 關閉
elif Sele == '3':
    action = 'forced_offline' # 強制關閉
elif Sele == '4':
    action = 'checked' # 檢查
else:
    action = "" # default value is none.
#
fail = mgmt.tm.sys.failover.load()
failOverStat = fail.apiRawValues['apiAnonymous'].rstrip()
#
fields = failOverStat.strip().split()
aabbcc = fields[1]
print( aabbcc )
#
pool_list = []
#pool_list.append(nodeMember + ":" + nodeMemberPort)
#
filename = input("請輸入讀取的檔案路徑和名稱 : ")
with open(filename, "r") as csv_file:
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

