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
#      Last modified: 2021-01-22 08:46
#     REVISION: ---
#===============================================================================
import sys
import re
import logging
import getpass
import time
from f5.bigip import ManagementRoot
import csv

path = 'output_data.csv'
#
#  Get login password from CLI
F5_host = input('F5_Host: ')
F5_user = input('Username: ')
F5_pw = getpass.getpass('Password: ')
#
mgmt = ManagementRoot(F5_host, F5_user, F5_pw)
# 檔案時間
dtf = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
filename = ("%s_Poolmember_IP_For_%s.csv" % (dtf, F5_host))
#sys.stdout=open("test.txt","w")
# CSV header
#print('Partition,VS_Name,Pool_Name,Pool_Members')
print('Partition,Pool_Name,Pool_Members')
pcsv =  open(filename, 'w', newline='')
#row_list = []
pcsv.write('Partition,Pool_Name,Pool_Members\n')
for pools in mgmt.tm.ltm.pools.get_collection():
#for virtual in mgmt.tm.ltm.virtuals.get_collection():
    # Does the virtual server have a pool assigned?
    #print("{}- -{}".format(pools.partition, pools.name))
    pool = mgmt.tm.ltm.pools.pool.load(
        partition=pools.partition,
        name=pools.name,
    )

    members = pool.members_s.get_collection()

    # Loop to output the results however you'd like
    # Example is CSV with pool members delimited by semicolon

    # Gather members in list - makes printing easier
    pool_members = []
    for member in members:
        pool_members.append("{}|{}".format(member.name, member.address))

    # Print result
    print('{},{},{}'.format(
        pools.partition,
        pool.name,
        ';'.join(pool_members),
    ))

    pcsv.write('{},{},{}\n'.format(
        pools.partition,
        pool.name,
        ';'.join(pool_members),
    ))

pcsv.close()
