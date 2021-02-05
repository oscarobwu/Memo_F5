#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_bigrest_v1.py
#
#        USAGE: f5_bigrest_v1.py
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
#      Created Time: 2021-01-19 15:17:50
#      Last modified: 2021-01-19 16:45
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
F5_Host_IP = "172.19.4.166"
f5_user = input('Username: ')
f5_pw = getpass.getpass('Password: ')


f5br = BIGIP(F5_Host_IP, f5_user, f5_pw, request_token=True)
p2 = f5br.load('/mgmt/tm/ltm/pool')
for p in p2:
    print(p.properties.get('name'))
    pirv = p.properties.get('name')
    pool = f5br.show(f"/mgmt/tm/ltm/pool/{rest_format(pirv)}")
    poolmem = f5br.load(f"/mgmt/tm/ltm/pool/{rest_format(pirv)}/members")
    for pm in poolmem:
        #print(pm.properties.get('name'))
        pmn = pm.properties.get('name')
        poolmemr = f5br.show(f"/mgmt/tm/ltm/pool/{rest_format(pirv)}/members/{rest_format(pmn)}")
        pmcurrent = poolmemr.properties["serverside.curConns"]["value"]
        print("\tpm-name : {} ,Current : {}".format(pmn, pmcurrent))


###
pools = f5br.load('/mgmt/tm/ltm/pool/?$select=name,loadBalancingMode')
for pl in pools:
    print(pl)


# Show virtual server information
# Show virtual server information
v2 = f5br.load('/mgmt/tm/ltm/virtual')
for v in v2:
    #print(v.properties.get('name'))
    virv = v.properties.get('name')
    virtual = f5br.show(f"/mgmt/tm/ltm/virtual/{rest_format(virv)}")
    max_conns = virtual.properties["clientside.maxConns"]["value"]
    print("\n {} - current : {} ".format(virv, max_conns))
    #if max_conns != 0:
    #    raise Exception(max_conns)
    #else:
    #    print(f"Virtual {virv} maximum number of connections.")
