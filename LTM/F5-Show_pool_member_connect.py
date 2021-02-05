#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       F5-Show_pool_member_connect.py
#
#        USAGE: F5-Show_pool_member_connect.py
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
#      Created Time: 2021-01-15 09:15:33
#      Last modified: 2021-01-15 09:15
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import datetime
import sys, getopt

#username = 'jenkins'
#password = 'jenkins'
username = sys.argv[4]
password = sys.argv[5]
host_ip = sys.argv[1]
fnames = sys.argv[2]
poolnames = sys.argv[3]
now = datetime.datetime.now()
mgmt = ManagementRoot(host_ip, username, password, token=True)

my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=(poolnames))

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
          print("%s  pool_member: [ %s ] 主機狀態 : \033[0;37;42m[ %s ]\033[0m 目前連線數 : \033[43m[ %s ]\033[0m" %(fnames, dic_test2, dic_btest1, dic_ctest1))
      elif (dic_dtest1 != 'disabled' or dic_btest1 != 'offline'):
          print("%s  pool_member: [ %s ] 主機狀態 : \033[0;37;41m[ %s ]\033[0m 目前連線數 : \033[43m[ %s ]\033[0m" %(fnames, dic_test2, dic_dtest1, dic_ctest1))
      elif (dic_btest1 == 'offline'):
          print("%s  pool_member: [ %s ] 主機狀態 : \033[0;37;41m[ %s ]\033[0m 目前連線數 : \033[43m[ %s ]\033[0m" %(fnames, dic_test2, dic_btest1, dic_ctest1))


print ( "\n" )
# vim:set nu et ts=4 sw=4 cino=>4:

