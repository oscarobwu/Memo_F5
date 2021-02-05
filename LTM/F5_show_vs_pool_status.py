#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       F5_show_vs_pool_status.py
#
#        USAGE: F5_show_vs_pool_status.py
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
#      Created Time: 2021-01-25 09:29:36
#      Last modified: 2021-01-25 09:37
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
from pprint import pprint
#  Get login password from CLI
F5_host = input('F5_Host: ')
F5_user = input('Username: ')
F5_pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, F5_user, F5_pw, token=True)
#
my_virtual = mgmt.tm.ltm.virtuals.virtual.load(partition='Common', name='my_virtual')
my_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name='my_pool')

v_stats = Stats(my_virtual.stats.load())
p_stats = Stats(my_pool.stats.load())

pprint(v_stats.stat)
pprint(p_stats.stat)
print(v_stats.stat.status_availabilityState)
print(p_stats.stat.status_availabilityState)
