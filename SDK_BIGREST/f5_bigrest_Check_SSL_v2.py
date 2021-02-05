#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_bigrest_Check_SSL_v1.py
#
#        USAGE: f5_bigrest_Check_SSL_v1.py
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
#      Created Time: 2021-01-19 17:42:09
#      Last modified: 2021-01-19 20:17
#     REVISION: ---
#===============================================================================
from bigrest.bigip import BIGIP
import getpass
import requests
import json
import sys
import time
import datetime
from pprint import pprint
requests.packages.urllib3.disable_warnings()
import os
import hashlib
# Internal imports
# Import only with "from x import y", to simplify the code.
#from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token
from dateutil.parser import parse


print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
#F5_Host_IP = input('F5_mgmt_IP: ')
F5_Host_IP = "172.19.4.166"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')


f5br = BIGIP(F5_Host_IP, f5_user, f5_pw, request_token=True)
# Show virtual server information
v2 = f5br.load('/mgmt/tm/sys/file/ssl-cert')
for v in v2:
    #print(v.properties.get('name'))
    #print("\t{}".format(v.properties.get('subjectAlternativeName')))
    tick = 0
    crt = 0
#    subnnn = v.properties.get('subjectAlternativeName')
#    exday = v.properties.get('expirationDate')
    expiration = parse(v.properties.get('expirationString'))
    #print(expiration)
    #print( '\t' + str((expiration.date() - datetime.date.today())) + '\t' + str(v.properties.get('name') + '\r' ))
    #if (((expiration.date() - datetime.date.today()).days <= 30 ) and ((expiration.date() - datetime.date.today()).days > 0 )):
    if ((expiration.date() - datetime.date.today()).days <= 30  ):
        tick = 1
        print( '\t' + str((expiration.date() - datetime.date.today())) + '\t' + str(v.properties.get('name') + '\r' ))
