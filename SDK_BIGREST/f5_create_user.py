#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_create_user.py
#
#        USAGE: f5_create_user.py
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
#      Created Time: 2021-01-19 20:35:16
#      Last modified: 2021-01-19 21:07
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
import getpass

#F5_Host_IP = input('F5_mgmt_IP: ')
F5_Host_IP = "172.19.4.166"

un = input('Username: ')
pw = getpass.getpass('Password: ')

mgmt = ManagementRoot(F5_Host_IP, un, pw )

name = input('Create Username: ')
password = getpass.getpass('Create Password: ')
mgmt.tm.auth.users.user.create(name=name, password=password, partitionAccess="all", shell="bash")
