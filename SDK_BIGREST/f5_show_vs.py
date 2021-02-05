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
#      Last modified: 2021-01-27 18:53
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
## Print virtual servers name
virtuals = device.load("/mgmt/tm/ltm/virtual")
print("List all virtual servers:")
for virtual in virtuals:
    print(virtual.properties["name"])
    print(virtual.properties["translatePort"])
    #print(virtual)
