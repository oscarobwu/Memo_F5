#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       test.py
#
#        USAGE: test.py
#
#  DESCRIPTION:關閉多台
#  python test.py pool_80_192.168.119.150 node_10.1.20.11:80,node_10.1.20.12:80
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Oscarob Wu(oscarobwu@gmail.com),
# ORGANIZATION:
#      VERSION: 1.0
#      Created Time: 2021-01-15 05:20:22
#      Last modified: 2021-01-15 05:30
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

pool_name = sys.argv[1]
#pool_member=sys.argv[1]
pool_member_list = list(sys.argv[2].split(','))
print(pool_name)
for x in pool_member_list:
    pool_member = '/Common/' + x
    data = {}
    #pool_name = "pool_8081_172.99.1.100"
    #pool_member = "/Common/node_10.99.0.11:8081"
    #Fource_Offline
    state = "user-down"
    session = "user-disabled"
    # Static
    data["state"] = state
    data["session"] = session
    pool_updated = device.modify(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(pool_member)}", data)
RTNETLINK answers: Network is unreachable
