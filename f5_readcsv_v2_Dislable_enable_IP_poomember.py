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
#      Last modified: 2021-01-25 15:56
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
#filename = input("請輸入讀取的檔案路徑和名稱 : ")
filename = "./2021-01-22-09-53_Poolmember_IP_For_172.19.4.166.csv"
with open(filename, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for lines in csv_reader:
        #result.append(record.split('-')[0])
        pmaddr = lines['Pool_Members']
        pmname = lines['Pool_Name']
        pmaddrsp = pmaddr.split(';')
        #pmaddrsp1 = [i.split('|')[1] for i in pmaddrsp]
        if aabbcc in ["active"]:
            for i in pmaddrsp:
                try:
                    pamaddrsp1 = i.split('|')[1]
                    pamaddrsp0 = i.split('|')[0]
                    if pamaddrsp1 in member_list:
                        #print("poolName :{} poomMember :{} poolMemberaddr: {}".format(pmname, pamaddrsp0, pamaddrsp1))
                        pooln = mgmt.tm.ltm.pools.pool.load(name=pmname, partition='Common')
                        #  pm1 = pooln.members_s.members.load(partition='Common', name=pamaddrsp0)
                        member = pooln.members_s.members.load(partition='Common', name=pamaddrsp0)
                        #fmember_stats = pooln.members_s.members.Stats(partition='Common', name=pamaddrsp0)
                        #my_pool_mbrs = pooln.members_s.get_collection()
                        my_pool_mbrs = pooln.members_s.get_collection()
                        # 
#                        for pool_mbr in my_pool_mbrs:
#                            #print(pool_mbr)
#                            if pamaddrsp0 in pool_mbr.name:
#                                mbr_stats = Stats(pool_mbr.stats.load())
#                                print(mbr_stats.stat.status_availabilityState)
#                                print(mbr_stats.stat.serverside_curConns)
                        #mmbr_stats = Stats(member.stats.load())
                        #my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=pmname)
                        pool_stats = Stats(pooln.stats.load())
                        #pmstats = member.stats.load()
                        #m_stats = Stats(member.stats.load())
                        #print(pool_stats.stat.status_availabilityState)
                        #pmmbrstatus = pmstats.stat.status_availabilityState['description']
                        #print("os tt : {}".format(pmmbrstatus))
                        currm = pool_stats.stat.availableMemberCnt['value']
                        if currm <= 1:
                            print(currm)
                            continue
                        else:
                            if action == 'enabled':
                                # enables member
                                #logger.info('開啟動作時狀態 member %s, previous state: %s' %
                                #                        (member.name, member.state))
                                member.state = 'user-up'
                                member.session = 'user-enabled'
                            elif action == 'disabled':
                                # disables member
                                #logger.info('關閉動作時狀態 member %s, previous state: %s' %
                                #                        (member.name, member.state))
                                member.session = 'user-disabled'
                            elif action == 'forced_offline':
                                # forces online member
                                #logger.info('強制關閉動作時狀態forces online member %s, previous state: %s' %
                                #                        (member.name, member.state))
                                member.state = 'user-down'
                                member.session = 'user-disabled'
                            elif action == 'checked':
                                # Checl online member
                                stt = member.session
                                #logger.info('checked online member %s, previous state: %s' %
                                #                        (member.name, member.state))
                                print('\t檢查 online member %s, previous state: %s' %
                                                        (member.name, member.state))
                                if "monitor-enabled" in stt:
                                    print('\t')
                                else:
                                    logger.info(另外一批有異常請檢查)
                                #print(False)

                            if action is not None:
                                member.update()
                                #
                                time.sleep(1)
                                for pool_mbr in my_pool_mbrs:
                                    #print(pool_mbr)
                                    if pamaddrsp0 in pool_mbr.name:
                                        mbr_stats = Stats(pool_mbr.stats.load())
                                        #print(mbr_stats.stat.status_availabilityState)
                                        mbrstatus = mbr_stats.stat.status_availabilityState['description']
                                        #print(mbr_stats.stat.serverside_curConns)
                                        #print('\t檢查的 member %s, 目前執行後狀態 : %s' %(member.name, mbr_stats.stat.status_availabilityState))
                                #print('\t檢查的 member %s, 目前執行後狀態 : %s' %(member.name, member.state))
                                print('\t檢查的 member %s, 目前執行後狀態 : %s' %(member.name, mbrstatus))
                                pool_list.append(pooln.name)
                            else:
                                logger.info('readonly mode, no changes applied')

                                logger.info('%s: %s %s' % (member.name, member.session, member.state))

                except:
                    continue

        else:
            print("this will do Nothing 請修改 Active F5 的 IP ")
            exit()
#
#
unique = []
for name in pool_list:         # 1st loop
    if name not in unique:   # 2nd loop
        unique.append(name)

#
print("\n")
now = datetime.datetime.now()
fnames = "開關機"
for x in unique:
    my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=(x))
    my_pool_mbrs = my_pool.members_s.get_collection()
    Count = 0
    print ( "\n" )
    print ("\033[0;37;44m\tCurrent Run date and time : \033[0m")
    print (now.strftime("\033[0;37;45m\t%Y-%m-%d %H:%M:%S\t\t\033[0m"))
    for pool_mbr in my_pool_mbrs:
        mbr_stats = Stats(pool_mbr.stats.load())
        dic_test = mbr_stats.stat.nodeName
        dic_test1 = dic_test['description']
        dic_test2 = dic_test1.replace('/Common/', '')
        dic_btest = mbr_stats.stat.status_availabilityState
        dic_btest1 = dic_btest['description']
        dic_ctest = mbr_stats.stat.serverside_curConns
        dic_ctest1 = dic_ctest['value']
        dic_dtest = mbr_stats.stat.status_enabledState
        dic_dtest1 = dic_dtest['description']
        Count = ((Count+1))
        #print ( "%s_%02d pool_member: [ %s ] 主機狀態 : %s  目前連線數 : \033[43m[ %s ]\033[0m" % (fnames, Count, dic_test2, dic_btest1,  dic_ctest1) )
        if (dic_btest1 == 'available' or dic_dtest1 != 'enabled' or dic_btest1 == 'offline'):
          if (dic_dtest1 == 'enabled' and dic_btest1 == 'available'):
              print("%s  pool_member: [ %s ] 主機狀態 : \033[0;37;42m[ %s ]\033[0m 目前連線數 : \033[43m[ %s ]\033[0m" %(x, dic_test2, dic_btest1, dic_ctest1))
          elif (dic_dtest1 != 'disabled' or dic_btest1 != 'offline'):
              print("%s  pool_member: [ %s ] 主機狀態 : \033[0;37;41m[ %s ]\033[0m 目前連線數 : \033[43m[ %s ]\033[0m" %(x, dic_test2, dic_dtest1, dic_ctest1))
          elif (dic_btest1 == 'offline'):
              print("%s  pool_member: [ %s ] 主機狀態 : \033[0;37;41m[ %s ]\033[0m 目前連線數 : \033[43m[ %s ]\033[0m" %(x, dic_test2, dic_btest1, dic_ctest1))


    print ( "\n" )
    # vim:set nu et ts=4 sw=4 cino=>4:
