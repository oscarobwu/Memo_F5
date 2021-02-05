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
#      Last modified: 2021-01-20 19:00
#     REVISION: ---
#===============================================================================
#  Standard Library
import sys
import re

#  Related Third-Party
import getpass

#  Local Application/Library Specific
from f5.bigip import ManagementRoot

#if len(sys.argv) < 4:
#print "\n\n\tUsage: %s host user node" % sys.argv[0]
#sys.exit()
#  Get login password from CLI
F5_host = input('F5_Host: ')
f5user = input('Username: ')
f5pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, f5user, f5pw)

#  Get list of pools and pool members
pools = mgmt.tm.ltm.pools.get_collection()
#nodesn =  mgmt.tm.ltm.nodes.get_collection()

buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        buffer.append(line)

print (buffer)
checkip = buffer
#  Node to search for
#Checknodes = []
#for nod in nodesn:
#    ips = nod.address
#    ipn = nod.name
#    Checknode = '/Common/' + ipn
#    Checknodes.append('/Common/' + ipn)
#    if ips in nodes:
#        print("{}, {}".format(ipn, ips))
#node = sys.argv[3]
#for node in nodes:
#    if len(node) < 8 or node[:8] != '/Common/':
#    #if len(node) < 8 or node[:8] != '/Common/':
#        node = '/Common/'+node
#        print("Pools using Node "+node)

print('\n')
for pooln in pools:
    #print(pooln.name)
    #print('\n')
    my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=pooln.name)
    #
    my_pool_mbrs = my_pool.members_s.get_collection()
    #
    for pool_mbr in my_pool_mbrs:
        #print('\n')
        if pool_mbr.address in checkip:
        #print(pool_mbr.address)
            print("{} MemberName : {}".format(pooln.name, pool_mbr.nam))

print("\n")
