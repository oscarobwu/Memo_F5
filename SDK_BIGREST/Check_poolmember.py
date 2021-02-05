#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       Check_poolmember.py
#
#        USAGE: Check_poolmember.py
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
#      Created Time: 2021-01-27 13:36:14
#      Last modified: 2021-01-27 13:47
#     REVISION: ---
#===============================================================================
###################################
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
# Add pool member
pool_name = "pool_80_172.97.1.99"
member_name = "/Common/node_10.99.0.20:80"
path = (
    f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}"
    f"/members/{rest_format(member_name)}"
)

# Test if poolmember not exists
if device.exist(path):
    print(f"poolmember {member_name} in {pool_name} exists.")
else:
    raise Exception(f"Creat poolmemeber {member_name} in {pool_name}.")
