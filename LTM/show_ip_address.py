#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       show_ip_address.py
#
#        USAGE: show_ip_address.py
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
#      Created Time: 2021-02-01 11:33:59
#      Last modified: 2021-02-01 12:38
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
from pprint import pprint
import getpass
#  Get login password from CLI
F5_host = input('F5_Host: ')
F5_user = input('Username: ')
F5_pw = getpass.getpass('Password: ')
#  Connect to BIG-IP
mgmt = ManagementRoot(F5_host, F5_user, F5_pw, token=True)
IPA = input('IPA: ')
#if mgmt.tm.ltm.nodes.node.exists(partition='Common', address=IPA):
a = mgmt.tm.ltm.nodes.node.load(partition='Common', name=IPA)
print(a.address)
#    node = mgmt.tm.ltm.nodes.node.load(partition='Common', address=IPA)
#    print(node.name)
