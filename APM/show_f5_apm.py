#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       show_f5_apm.py
#
#        USAGE: show_f5_apm.py
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
#      Created Time: 2021-01-13 17:40:00
#      Last modified: 2021-01-13 17:54
#     REVISION: ---
#===============================================================================
import getpass
import requests
requests.packages.urllib3.disable_warnings()

print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
F5_Host_IP = input('F5_mgmt_IP: ')
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')

from f5.bigip import ManagementRoot
# Basic Authentication
#b = ManagementRoot('ltm3.test.local', 'admin', 'admin')
# Token Authentication
b = ManagementRoot(F5_Host_IP, f5_user, f5_pw, token=True)
#ver = b.tmos_version
#print(ver)
# The Net/Vlan Collection:
#vlans = b.tm.net.vlans.get_collection()
#for vlan in vlans:
#    print (vlan.name)
for x in b.tm.apm.get_collection():
    print (x)
