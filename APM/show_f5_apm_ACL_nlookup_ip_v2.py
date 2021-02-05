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
#      Last modified: 2021-01-14 18:28
#     REVISION: ---
#===============================================================================
from bigrest.bigip import BIGIP
import getpass
import requests
import json
import sys
from pprint import pprint
requests.packages.urllib3.disable_warnings()

print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
#F5_Host_IP = input('F5_mgmt_IP: ')
F5_Host_IP = "172.19.37.248"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')
#
print('檢查IP: ')
#stopword = ''
#str = ''
#ip_input = ''
#count = 0
#for line in iter(input,stopword):
#    count = count + 1
#    ip_input+=line+','
#
ip_lists = []
while True:
    s = input("輸入檢查 the IP address or press ENTER for Output: ")
    if s:
        ip_lists.append(s)
    else:
        break;
#
print(ip_lists)
device = BIGIP(F5_Host_IP, f5_user, f5_pw)
APM_ACL = device.load("/mgmt/tm/apm/acl")
count = 0
aaacls = []
for acls in APM_ACL:
    #print(acls)
    #print(acls.properties['entries'])
    count = count + 1
    n = acls.properties["name"]
    od = acls.properties["aclOrder"]
    #print("\n{}. ACL_Name : {}".format(count, n))
    for k, v in acls.properties.items():
        #print(k)
        #print("\n{}. ACL_Name : {}".format(count, n))
        if k == 'entries':
            try:
                #print("\n{}. ACL_Name {} : {}".format(count, od, n))
                for xxx in acls.properties["entries"]:
                    #aaa = resp_dict.get('dstSubnet')
                    a1 = xxx['action']
                    a2 = xxx['dstEndPort']
                    a3 = xxx['dstStartPort']
                    a4 = xxx['dstSubnet']
                    ipp = a4.split('/')[0]
                    #print("\n{}. ACL_Name : {}".format(count, n))
                    #for inipaddr in ip_input.split(',')[:-1]:
                    #print("\n{}. ACL_Name : {}".format(count, n))
                    acls_list = []
                    #print("\n{}. ACL_Name : {}".format(count, n))
                    if ipp in ip_lists:
                        #print("\n{}. ACL_Name : {}".format(count, n))
                        acls_list.append("\tDstIP :{}, DstPort : {}, Action : {} ".format(a4, a3, a1))
                        #aaacls.append("DstIP :{}, DstPort : {}, Action : {};".format(a4, a3, a1))

                    # Print result
                        print('{} ACL_Name: {},\n{}'.format(
                            count,
                            n,
                            ';'.join(acls_list),
                        ))
            except:
                  print("exceot")
#
#for i in aaacls:
#	#t = i.split(';')
#	print(i)
#print([i.split(';') for i in aaacls])
