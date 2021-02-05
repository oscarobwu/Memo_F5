#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       show_f5_apm_v2.py
#
#        USAGE: show_f5_apm_v2.py
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
#      Created Time: 2021-01-13 21:23:33
#      Last modified: 2021-01-14 10:21
#     REVISION: ---
#===============================================================================
from bigrest.bigip import BIGIP
import getpass
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
#F5_Host_IP = input('F5_mgmt_IP: ')
F5_Host_IP = "172.19.37.248"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')
#
device = BIGIP(F5_Host_IP, f5_user, f5_pw)
APM_ACL = device.load("/mgmt/tm/apm/acl")
count = 0
for acls in APM_ACL:
#    print(acls)
    #print(acls.properties['entries'])
    count = count + 1
    n = acls.properties["name"]
    print("\n{}. ACL_Name : {}".format(count, n))
    for k, v in acls.properties.items():
        #print(k)
        if k == 'entries':
            #print("find the word")
            #print("\n{}. ACL_Name : {}".format(count, n))
            #count = count + 1
            #print(acls)
            for xxx in acls.properties["entries"]:
                #aaa = resp_dict.get('dstSubnet')
                a1 = xxx['action']
                a2 = xxx['dstEndPort']
                a3 = xxx['dstStartPort']
                a4 = xxx['dstSubnet']
                print ("\tDstIP :{}, DstPort : {}, Action : {} ".format(a4, a3, a1))

#            print("\n {}".format(n))
#        if v.get('entries') != None:
#            print(f'{k}: {v.get("entries")}')
#    for k, v in acls.properties.items() :
#        #print("{}, {}".format(k, v))
#        if k.get('entries') != None:
#            print("SubPath: {}".format(acls.properties["name"]))
#        else:
#            print("SubPath: None")
