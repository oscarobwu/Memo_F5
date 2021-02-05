#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       show_f5_apm_v1.py
#
#        USAGE: show_f5_apm_v1.py
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
#      Created Time: 2021-01-13 18:43:32
#      Last modified: 2021-01-13 21:16
#     REVISION: ---
#===============================================================================
from bigrest.bigip import BIGIP
import getpass
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
F5_Host_IP = input('F5_mgmt_IP: ')
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')
#
device = BIGIP(F5_Host_IP, f5_user, f5_pw)
APM_ACL = device.load("/mgmt/tm/apm/acl")
for acls in APM_ACL:
    n = acls.properties["name"]
    #if not getattr(acls, 'entries', None):
    if hasattr(acls, 'entries'):
        # No - print virtual server name and move on
        print("\nName : {} entr_ACL : ".format(n))
        for xxx in acls.properties["entries"]:
            #aaa = resp_dict.get('dstSubnet')
            a1 = xxx['action']
            a2 = xxx['dstEndPort']
            a3 = xxx['dstStartPort']
            a4 = xxx['dstSubnet']
            print ("\tDstIP :{}, DstPort : {}, Action : {} ".format(a4, a3, a1))
        continue
    else:
    #e = acls.properties["entries"]
        print("\nName : {} entr_ACL : ".format(n))
#    for xxx in acls.properties["entries"]:
#        #aaa = resp_dict.get('dstSubnet')
#        a1 = xxx['action']
#        a2 = xxx['dstEndPort']
#        a3 = xxx['dstStartPort']
#        a4 = xxx['dstSubnet']
#        print ("\tDstIP :{}, DstPort : {}, Action : {} ".format(a4, a3, a1))
