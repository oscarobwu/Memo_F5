#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       show_nod_ipaddr.py
#
#        USAGE: show_nod_ipaddr.py
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
#      Created Time: 2021-02-02 11:47:57
#      Last modified: 2021-02-02 16:41
#     REVISION: ---
#===============================================================================
import getpass
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
from pprint import pprint
#  Get login password from CLI
F5_host = input('F5_Host: ')
F5_user = input('Username: ')
F5_pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, F5_user, F5_pw, token=True)
IPA = input('IPA: ')
#nodes = mgmt.tm.ltm.nodes.get_collection()
#for m in nodes:
#    if m.address==IPA:
#        print(m.name)


if mgmt.tm.ltm.nodes.node.exists(address=IPA):
	print("True")
