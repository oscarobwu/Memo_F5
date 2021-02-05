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
#      Last modified: 2021-01-22 12:20
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
#F5_host = input('F5_Host: ')
f5user = input('Username: ')
f5pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
#mgmt = ManagementRoot(F5_host, f5user, f5pw)
#
#  Get list of pools and pool members
#pools = mgmt.tm.ltm.pools.get_collection()
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
#fail = mgmt.tm.sys.failover.load()
#failOverStat = fail.apiRawValues['apiAnonymous'].rstrip()
#
#fields = failOverStat.strip().split()
#aabbcc = fields[1]
#print( aabbcc )
#
pool_list = []
#pool_list.append(nodeMember + ":" + nodeMemberPort)
#
filename = input("請輸入讀取的檔案路徑和名稱 : ")
with open(filename, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for lines in csv_reader:
        #result.append(record.split('-')[0])
        F5MGMT = lines['F5_host']
        pmaddr = lines['Pool_Members']
        pmname = lines['Pool_Name']
        pmaddrsp = pmaddr.split(';')
        #pmaddrsp1 = [i.split('|')[1] for i in pmaddrsp]
        mgmt = ManagementRoot(F5MGMT, f5user, f5pw)
        fail = mgmt.tm.sys.failover.load()
        failOverStat = fail.apiRawValues['apiAnonymous'].rstrip()
        #
        fields = failOverStat.strip().split()
        aabbcc = fields[1]
        #print( aabbcc )
        if aabbcc in ["active"]:
            for i in pmaddrsp:
                try:
                    pamaddrsp1 = i.split('|')[1]
                    pamaddrsp0 = i.split('|')[0]
                    if pamaddrsp1 in member_list:
                        mgmt = ManagementRoot(F5MGMT, f5user, f5pw)
                        print("F5_MGMT: {} poolName :{} poomMember :{} poolMemberaddr: {}".format(F5MGMT, pmname, pamaddrsp0, pamaddrsp1))
                        #print("poolName :{} poomMember :{} poolMemberaddr: {}".format(pmname, pamaddrsp0, pamaddrsp1))
                        pooln = mgmt.tm.ltm.pools.pool.load(name=pmname, partition='Common')
                        #pm1 = pooln.members_s.members.load(partition='Common', name=pamaddrsp0)
                        member = pooln.members_s.members.load(partition='Common', name=pamaddrsp0)
                        #my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=pmname)
                        pool_stats = Stats(pooln.stats.load())
                        #print(pool_stats.stat.status_availabilityState)
                        currm = pool_stats.stat.availableMemberCnt['value']
                        if currm <= 1:
                            print(currm)
                            continue
                        else:
                            if action == 'enabled':
                                # enables member
                                logger.info('enables member %s, previous state: %s' %
                                                        (member.name, member.state))
                                member.state = 'user-up'
                                member.session = 'user-enabled'
                            elif action == 'disabled':
                                # disables member
                                logger.info('disables member %s, previous state: %s' %
                                                        (member.name, member.state))
                                member.session = 'user-disabled'
                            elif action == 'forced_offline':
                                # forces online member
                                logger.info('forces online member %s, previous state: %s' %
                                                        (member.name, member.state))
                                member.state = 'user-down'
                                member.session = 'user-disabled'
                            elif action == 'checked':
                                # Checl online member
                                stt = member.session
                                #logger.info('checked online member %s, previous state: %s' %
                                #                        (member.name, member.state))
                                print('\tchecked online member %s, previous state: %s' %
                                                        (member.name, member.state))
                                if "monitor-enabled" in stt:
                                    print('\t')
                                else:
                                    logger.info(另外一批有異常請檢查)
                                #print(False)

                            if action is not None:
                                member.update()
                                print('\t檢查的 member %s, 目前執行後狀態 : %s' %(member.name, member.state))
                                pool_list.append(poolna.name)
                            else:
                                logger.info('readonly mode, no changes applied')

                                logger.info('%s: %s %s' % (member.name, member.session, member.state))

                except:
                    continue

        else:
            print("this will do Nothing 請修改 Active F5 的 IP ")
            exit()
#
