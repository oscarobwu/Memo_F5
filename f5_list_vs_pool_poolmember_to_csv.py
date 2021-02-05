#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_list_vs_pool_poolmember_to_csv.py
#
#        USAGE: f5_list_vs_pool_poolmember_to_csv.py
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
#      Created Time: 2021-01-21 11:25:40
#      Last modified: 2021-01-21 11:29
#     REVISION: ---
#===============================================================================
import sys
import re
import logging
import getpass
import time
from f5.bigip import ManagementRoot
#
#  Get login password from CLI
F5_host = input('F5_Host: ')
F5_user = input('Username: ')
F5_pw = getpass.getpass('Password: ')
#
mgmt = ManagementRoot(F5_host, F5_user, F5_pw)

# CSV header
print('Partition,VS_Name,Pool_Name,Pool_Members')

for virtual in mgmt.tm.ltm.virtuals.get_collection():
    # Does the virtual server have a pool assigned?
    if not getattr(virtual, 'pool', None):
        # No - print virtual server name and move on
        print('{},{},,'.format(virtual.partition, virtual.name))
        continue

    # Pool partition
    pool_part = virtual.pool.split('/')[1]
    # Pool name
    pool_name = virtual.pool.split('/')[2]

    pool = mgmt.tm.ltm.pools.pool.load(
        partition=pool_part,
        name=pool_name,
    )

    members = pool.members_s.get_collection()

    # Loop to output the results however you'd like
    # Example is CSV with pool members delimited by semicolon

    # Gather members in list - makes printing easier
    pool_members = []
    for member in members:
        pool_members.append(member.name)

    # Print result
    print('{},{},{},{}'.format(
        virtual.partition,
        virtual.name,
        pool.name,
        ';'.join(pool_members),
    ))
