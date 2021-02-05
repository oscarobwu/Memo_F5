#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       test.py
#
#        USAGE: test.py
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
#      Created Time: 2021-01-15 05:20:22
#      Last modified: 2021-01-15 07:56
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
#F5_Host_IP = input('F5_mgmt_IP: ')
F5_Host_IP = "192.168.101.167"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')

device = BIGIP(F5_Host_IP, f5_user, f5_pw)
count = 0
#pool_name = sys.argv[1]
#pool_member=sys.argv[1]
#pool_member_list = list(sys.argv[2].split(','))
#print(pool_name)
#for x in pool_member_list:
#    pool_member = '/Common/' + x
#    data = {}
#    #pool_name = "pool_8081_172.99.1.100"
#    #pool_member = "/Common/node_10.99.0.11:8081"
#    #Fource_Offline
#    state = "user-down"
#    session = "user-disabled"
#    # Static
#    data["state"] = state
#    data["session"] = session
#    pool_updated = device.modify(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(pool_member)}", data)

#
pools_list = device.load('/mgmt/tm/ltm/pool')
for pool in pools_list:
    pool_name = pool.properties['name']
#    pool_member_list = device.load(f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members')
    n = pool.properties["name"]
    print(n)
    for pool_name_s in n.split():
#        pool_member_n = pool_member_s.properties["name"]
        print(pool_name_s)
        poolmemberlist = device.load(f'/mgmt/tm/ltm/pool/{rest_format(pool_name_s)}/members')
        #print(poolmemberlist)
        for x in poolmemberlist:
            print(x.properties['name'])
            members = x.properties['name']
            pool_member_stats = device.show(f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(members)}')
            for p in pool_member_stats:
                for k, v in p.properties.items():
                    if v.get('description') != None:
                        print(f'{k}: {v.get("description")}')
                    elif v.get('value') != None:
                        print(f'{k}: {v.get("value")}')
#
#        print(pool_member_n)
#opoolstats = device.show('/mgmt/tm/ltm/pool')
#pool_name = "pool_80_192.168.119.150"
#pool_member_stats = device.load(f'/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members')
#for pool in pool_member_stats:
#    count = count + 1
#    #print(pool)
#    n = pool.properties["name"]
#    print(n)
#    #od = pool.properties["aclOrder"]
#    for k, v in pool.properties.items():
#        print(k)
        #print(k)
        #print("\n{}. ACL_Name : {}".format(count, n))
#        if k == 'entries':
#            try:
#                #print("\n{}. ACL_Name {} : {}".format(count, od, n))
#                for k, v in p.properties.items():
#                    if v.get('description') != None:
#                        print(f'{k}: {v.get("description")}')
#                    elif v.get('value') != None:
#                        print(f'{k}: {v.get("value")}')
#
#            except:
#                  print("exceot")
#for p in pool_member_stats:
#       print(p)
#    for k, v in p.properties.items():
#         print(k)
#        if v.get('description') != None:
#            print(f'{k}: {v.get("description")}')
#        elif v.get('value') != None:
#            print(f'{k}: {v.get("value")}')

#pools_list = device.load('/mgmt/tm/ltm/pool')
#for pool in pools_list:
#    pool_name = pool.properties['name']
#    print(pool_name)
#    pool_member_stats = device.show('/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members')
#    for p in pool_member_stats:
#        for k, v in p.properties.items():
#            if v.get('description') != None:
#                print(f'{k}: {v.get("description")}')
#            elif v.get('value') != None:
#                print(f'{k}: {v.get("value")}')
#RTNETLINK answers: Network is unreachable
# 顯示pool member 連線數
# current_pool_conntion = pool_member.properties["serverside.maxConns"]["value"]
