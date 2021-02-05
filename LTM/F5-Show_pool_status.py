#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       F5-Show_pool_status.py
#
#        USAGE: F5-Show_pool_status.py
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
#      Created Time: 2021-01-25 14:50:13
#      Last modified: 2021-01-25 14:56
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
import getpass

def get_pool_stats(p_name, p_partition):
    """Return all pool stats object (dict of dicts)"""
    pool = API_ROOT.tm.ltm.pools.pool.load(name=p_name, partition=p_partition)
    return pool.stats.load()

print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
F5_Host_IP = input('F5_mgmt_IP: ')
#F5_Host_IP = "172.19.37.248"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')

API_ROOT = ManagementRoot(F5_Host_IP, f5_user, f5_pw)
POOL_STATS = get_pool_stats('pool_8081_172.99.1.100', 'Common')

# EXAMPLES OF USE:

# 1. Print all stats (complete dictionary of dictionaries, inclusive of irrelevant bulk)
print(POOL_STATS.raw)
# 2. Print all stats (entries dictionary - all key/value pairs of actual stats)
print(POOL_STATS.entries)
# 3. Print a specific extraction from entries dictionary
print(POOL_STATS.entries.get('curSessions'))
# 4. Print a specific extraction from entries dictionary (just value of a specific key)
print(POOL_STATS.entries.get('curSessions')['value'])
