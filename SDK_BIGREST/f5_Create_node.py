#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_Create_node.py
#
#        USAGE: f5_Create_node.py
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
#      Last modified: 2021-01-27 10:36
#     REVISION: ---
#===============================================================================
# External Imports
# Import only with "import package",
# it will make explicity in the code where it came from.
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
print("Username: ", end="")
F5_username = input()
F5_password = getpass.getpass('Password: ')
print("Device IP or name: ", end="")
F5_Host = input()
#print("Node_ip : ", end="")
#node_ip_address = input()
print('請輸入資料_IP_Address，直接按下Enter 結束 : ')
buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        buffer.append(line)
#print (buffer)
node_list = buffer

# Create a device object with basic authentication
device = BIGIP(F5_Host, F5_username, F5_password)

# Create node
for node_ip_address in node_list:
    node_name = 'node_' + node_ip_address
    if device.exist(f"/mgmt/tm/ltm/node/{rest_format(node_name)}"):
        print(f"Node {node_name} exists.")
    else:
        raise Exception(f"Create {node_name} and Check not exists.")
        data = {}
        data["name"] = node_name
        data["address"] = node_ip_address
        data["description"] = 'webserver_NS2020-1026-001'
        node = device.create(
            f"/mgmt/tm/ltm/node/", data)
        if node.properties["fullPath"] != '/Common/' + 'node_' + node_ip_address:
            raise Exception(node.properties["fullPath"])
        else:
            print(f"Node {node_ip_address} created.")
