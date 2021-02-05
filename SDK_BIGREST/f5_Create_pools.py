#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:      f5_Create_node_pool_add_member_v1.py 
#
#        USAGE: f5_Create_node_pool_add_member_v1.py
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
#      Created Time: 2021-01-27 09:35:46
#      Last modified: 2021-01-27 12:54
#     REVISION: ---
#===============================================================================
import getpass
import os
import hashlib
import sys

# Internal imports
# Import only with "from x import y", to simplify the code.
from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token

# Get username, password, and ip
F5_Host = input('Device IP or name: ')
print("Username: ", end="")
F5_username = input()
F5_password = getpass.getpass('Password: ')
#print("Device IP or name: ", end="")
# Create a device object with basic authentication
device = BIGIP(F5_Host, F5_username, F5_password)
partition_name = "/Common/"
#
Job_name = input('輸入單號或說明: ')
#print("Node_ip : ", end="")
#node_ip_address = input()

VIP_address = input('VIP Address: ')

print('請輸入資料 port list，如 \n80\n443\n8080\n...直接按下Enter 結束 : ')
port_buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        port_buffer.append(line)
#print (buffer)
port_list = port_buffer

# Create pool
for pools in port_list:
    pool_names = 'pool_' + pools + '_' + VIP_address
    if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_names)}"):
        print(f"Pool {pool_names} exists.")
    else:
        #raise Exception(f"Create {pool_names} and Check not exists.")
        data = {}
        data["name"] = pool_names
        print(pool_names)
        data["description"] = Job_name
        pool = device.create("/mgmt/tm/ltm/pool", data)
        if pool.properties["fullPath"] != '/Common/' + pool_names:
            raise Exception(pool.properties["fullPath"])
        else:
            print(f"Pool {pool_names} created.")


## Add pool member
#for port in port_list:
#    pool_name = 'pool_' + port + '_' + VIP_address
#    for members in node_list:
#        member_name = 'node_' + members + ':' + port
#        # Test if poolmember not exists
#        if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(member_name)}"):
#            print(f"poolmember {member_name} in {pool_name} exists.")
#        else:
#            raise Exception(f"Creat poolmemeber {member_name} in {pool_name}.")
#            data = {}
#            data["name"] = member_name
#            member = device.create(
#                f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members", data)
#            if member.properties["fullPath"] != '/Common/' + member_name:
#                raise Exception(member.properties["fullPath"])
#            else:
#                print(f"Member {member_name} created.")
