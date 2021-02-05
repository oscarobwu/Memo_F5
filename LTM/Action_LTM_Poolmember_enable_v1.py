#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       show_LTM_Pool_v1.py
#
#        USAGE: show_LTM_Pool_v1.py
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
#      Created Time: 2021-01-14 19:43:32
#      Last modified: 2021-01-14 20:46
#     REVISION: ---
#===============================================================================
from bigrest.bigip import BIGIP
import getpass
import requests
import json
import sys
from pprint import pprint
requests.packages.urllib3.disable_warnings()
import os
import hashlib
# Internal imports
# Import only with "from x import y", to simplify the code.
#from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token


print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
F5_Host_IP = input('F5_mgmt_IP: ')
#F5_Host_IP = "172.19.37.248"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')

device = BIGIP(F5_Host_IP, f5_user, f5_pw)


# Print Pool name
#pools = device.load("/mgmt/tm/ltm/pool")
#print("List all Pool list:")
#for pool in pools:
#    print(pool.properties["name"])
#    pool_n = pool.properties["name"]
#    member = device.load(f"/mgmt/tm/ltm/pool/{rest_format(pool_n)}/members")
#    for pool_member in member:
#        print("\t {}".format(pool_member.properties["name"]))
## Print node example
#nodes = device.load(f"/mgmt/tm/ltm/node")
#print("Print node example:")
#for node in nodes:
#`    print(node.properties["name"])
# Modify pool description
data = {}
#Fource_Offline
pool_name = "pool_8081_172.99.1.100"
pool_member = "/Common/node_10.99.0.11:8081"
state = "user-up"
session = "user-enabled"
data["state"] = state
data["session"] = session
pool_updated = device.modify(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(pool_member)}", data)
