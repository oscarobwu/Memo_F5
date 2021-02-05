#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       List_commands_to_grab_VIPs_and_Pool_members.py
#
#        USAGE: List_commands_to_grab_VIPs_and_Pool_members.py
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
#      Created Time: 2021-01-12 07:57:05
#      Last modified: 2021-01-13 12:09
#     REVISION: ---
#===============================================================================
import getpass
from f5.bigip import ManagementRoot
#
f5_host = input('F5_mgmt_IP: ')
#f5_host = '192.168.8.168'
print("登入 主機 : %s" % f5_host)
f5_user = input('\nUsername: ')
f5_pw = getpass.getpass('\nPassword: ')
#
mgmt = ManagementRoot(f5_host, f5_user, f5_pw)
 
# CSV header
print('Partition, VS Name, Pool Name, Pool Members')
 
for virtual in mgmt.tm.ltm.virtuals.get_collection():
    # Does the virtual server have a pool assigned?
    if not getattr(virtual, 'pool', None):
        # No - print virtual server name and move on
        print('{},{},'.format(virtual.partition, virtual.name))
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
