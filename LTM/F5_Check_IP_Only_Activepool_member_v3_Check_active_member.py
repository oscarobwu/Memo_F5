#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       F5_Check_IP_Action_pool_member_v2_Check_active_member.py
#
#        USAGE: F5_Check_IP_Action_pool_member_v2_Check_active_member.py
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
#      Created Time: 2021-01-20 08:10:02
#      Last modified: 2021-01-20 08:20
#     REVISION: ---
#===============================================================================
__author__ = 'oscarwu'
__version__ = '1.0'

#  Standard Library
import sys
import re
import logging
import getpass
#  Local Application/Library Specific
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import datetime
import sys, getopt

if len(sys.argv) < 1:
    print( "\n\n\tUsage: %s host user node" % sys.argv[0])
    sys.exit()

#  Get login password from CLI
F5_host = input('F5_Host: ')
f5user = input('Username: ')
f5pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, f5user, f5pw)

#  Get list of pools and pool members
pools = mgmt.tm.ltm.pools.get_collection()
FORMAT = '%(asctime)s %(levelname)s %(module)s %(message)s'
logging.basicConfig(format=FORMAT, level='INFO')
logger = logging.getLogger('set_pool_members_state')
#  Node to search for
node = input('Node_清單使用,分隔_10.99.0.11,10.99.0.12,10.99.0.13\nIPaddress: ')
member_list = node.split(',')
#action = sys.argv[1]
#action = input('[enabled, disabled, forced_offline, checked] : ')
print("選擇開關機的方式?\n")
print("[1] enabled\n")
print("[2] checked\n")
Sele = input("Your choice (press enter to skip): ")
if Sele == '1':
    action = 'enabled' # 開啟
elif Sele == '2':
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
for poolna in pools:
    #print(poolna.name)
    my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=poolna.name)
    pool_stats = Stats(my_pool.stats.load())
    #print(pool_stats.stat.status_availabilityState)
    currm = pool_stats.stat.availableMemberCnt['value']
    member_nodes = [member.fullPath.split(':')[0] for member in poolna.members_s.get_collection()]
    member_nodes_name = [member.name for member in poolna.members_s.get_collection()]
    #
    member_address = [member.address for member in poolna.members_s.get_collection()]
    #
    member = poolna.members_s.get_collection()
    for nod_ip in member:
        ckip = nod_ip.address
        for node_list in member_list:
            if node_list in ckip:
                print( "\t"+poolna.name + "\t" + nod_ip.name )
                pooln = mgmt.tm.ltm.pools.pool.load(name=poolna.name, partition='Common')
                pm1 = pooln.members_s.members.load(partition='Common', name=nod_ip.name)
                if aabbcc in ["active"]:
                    for member in [pm1]:
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
                else:
                    print("this will do Nothing 請修改 Active F5 的 IP ")
                    exit()
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
