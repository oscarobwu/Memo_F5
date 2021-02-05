#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       check_nodeip.py
#
#        USAGE: check_nodeip.py
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
#      Created Time: 2021-01-20 14:46:39
#      Last modified: 2021-01-20 19:09
#     REVISION: ---
#===============================================================================
#  Standard Library
import sys
import re

#  Related Third-Party
import getpass

#  Local Application/Library Specific
from f5.bigip import ManagementRoot

#  Get login password from CLI
F5_host = input('F5_Host: ')
f5user = input('Username: ')
f5pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, f5user, f5pw)

#  Get list of pools and pool members
pools = mgmt.tm.ltm.pools.get_collection()
#
buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        buffer.append(line)

print (buffer)
checkip = buffer
#
fail = mgmt.tm.sys.failover.load()
failOverStat = fail.apiRawValues['apiAnonymous'].rstrip()
#
fields = failOverStat.strip().split()
aabbcc = fields[1]
print(aabbcc)
#
print('\n')
for pooln in pools:
    #print('\n')
    my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=pooln.name)
    #
    my_pool_mbrs = my_pool.members_s.get_collection()
    #
    for pool_mbr in my_pool_mbrs:
        #print('\n')
        if pool_mbr.address in checkip:
        #print(pool_mbr.address)
            print("{} \tMemberName : {}".format(pooln.name, pool_mbr.name))

#print("\n")
