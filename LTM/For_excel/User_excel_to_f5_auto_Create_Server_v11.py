#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       User_excel_to_f5_auto_Create_Server_v2.py
#
#        USAGE: User_excel_to_f5_auto_Create_Server_v2.py
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
#      Created Time: 2021-01-29 14:32:04
#      Last modified: 2021-02-01 20:59
#     REVISION: ---
#===============================================================================
import requests
import json
from requests.packages import urllib3
from nacl.pwhash import verify
import xlrd
import openpyxl
import pandas as pd
from xpinyin import Pinyin
from idlelib.iomenu import encoding
import getpass
import time
import os
from netaddr import IPNetwork, IPAddress
# Internal imports
# Import only with "from x import y", to simplify the code.
from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token

#
p = Pinyin()
urllib3.disable_warnings()   #disable ssl warning
# System call
os.system("")

# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.YELLOW + "Hello, World!" + '\033[0m')

#導入excel數據    ------begin----------
config_file = input("請輸入需要導入的excel表格名稱，請帶尾碼如：配置資訊.xlsx，\n設定檔請放在python腳本一個資料夾下 : ")
data = pd.read_excel(config_file, sheet_name=0, engine='openpyxl', keep_default_na=False)
#
print(data)
member = pd.DataFrame(data, columns=["App_Name", "Create_Date", "Description", "type", "VIP", "VIP_port", "pool_member_ip", "pool_member_port"])
appv = member.values
count = 0
print("\n")

#導入excel數據  --------end-----------

#dcreate auth token
f5_ip = input("請輸入F5管理IP   : ")
username = input("請輸入F5管理帳戶 : ")
password = getpass.getpass("請輸入F5管理密碼 : ")
#
# Create a device object with basic authentication
device = BIGIP(f5_ip, username, password)
#
req_url = 'https://%s/mgmt/shared/authn/login' %(f5_ip)
data = {'username':username,
        'password':password,
        'loginProviderName':'tmos'
        }
r = requests.post(req_url,json.dumps(data),verify = False)
#
#get auth token
f5_rep = json.loads(r.text)
f5_token = f5_rep['token']['token']
#
#header for connection f5
creat_header = {
    'X-F5-Auth-Token':f5_token,
    'Content-Type':'application/json'
    }
#
for l in appv:
    count = count + 1
    poolname = l[0]
    Descrip = l[2]
    t = l[4]
    vip_addr = l[4]
    vip_port = l[5]
    if poolname != '':
        monic_name = 'TCP-' + str(vip_port)
        if device.exist(f"/mgmt/tm/ltm/monitor/tcp/{rest_format(monic_name)}"):
            print(style.RED + f"monitor {monic_name} exists." + '\033[0m')
        else:
            #raise Exception(f"monitor {member_name} in {pool_name}.")
            data = {}
            data["name"] = monic_name
            data["destination"] = '*.' + str(vip_port)
            monitor = device.create(
                f"/mgmt/tm/ltm/monitor/tcp", data)
            if monitor.properties["fullPath"] != '/Common/' + monic_name:
                raise Exception(monitor.properties["fullPath"])
            else:
                print(f"Health Monitor {monic_name} created.")
#
        pool_names = 'pool_' + str(vip_port) + '_' + vip_addr
        if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_names)}"):
            print(style.RED + f"Pool {pool_names} exists." + '\033[0m')
        else:
            #raise Exception(f"Create {pool_names} and Check not exists.")
            if vip_port == '80' or vip_port == '443':
                monitor_name = "/Common/http"
            else:
                monitor_name = '/Common/TCP-' + str(vip_port)
            data = {}
            data["name"] = pool_names
            data["description"] = Descrip
            data["monitor"] = monitor_name
            print(pool_names)
            #data["description"] = Job_name
            pool = device.create(f"/mgmt/tm/ltm/pool", data)
            if pool.properties["fullPath"] != '/Common/' + pool_names:
                raise Exception(pool.properties["fullPath"])
            else:
                print(f"Pool {pool_names} created.")
    else :
        continue

print("\nAdd Pool member\n")
##members into pool
partition_name = "/Common/"
pool_name_last = []
descia = []
for l in appv:
    count = count + 1
    poolname = l[0]
    vip_addr = l[4]
    vip_port = l[5]
    Descrip = l[2]
    pmb_ip = l[6]
    pmb_port = l[7]
    if Descrip == '':
        desc = descia[-1:][0]
    else:
        desc = Descrip
        descia.append(Descrip)
    # Create node
    node_name = 'node_' + pmb_ip
    if device.exist(f"/mgmt/tm/ltm/node/{rest_format(node_name)}"):
        print(style.RED + f"Node {node_name} exists." + '\033[0m')
    else:
        data = {}
        data["name"] = node_name
        data["address"] = pmb_ip
        data["description"] = desc
        node = device.create(f"/mgmt/tm/ltm/node/", data)
        if node.properties["fullPath"] != '/Common/' + 'node_' + pmb_ip:
            raise Exception(node.properties["fullPath"])
        else:
            print(f"Node {pmb_ip} created.")
    #print(pool_name_last)
    name_to_py = p.get_pinyin("pool_{}_{}".format(vip_port, vip_addr))
    if vip_addr == '':
        pool_name = pool_name_last[-1:][0]
    else:
        pool_name = "pool_{}_{}".format(vip_port, vip_addr)
        pool_name_last.append("pool_%s_%s" % (vip_port, vip_addr))
        time.sleep(1)
    member_name = 'node_' + pmb_ip + ':' + str(pmb_port)
    pmember_name = partition_name + 'node_' + pmb_ip + ':' + str(pmb_port)
    # Test if poolmember not exists
    print(pool_name)
    if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(pmember_name)}"):
        print(style.RED + f"poolmember {member_name} in {pool_name} exists." + '\033[0m')
    else:
        #raise Exception(f"Creat poolmemeber {member_name} in {pool_name}.")
        data = {}
        data["name"] = member_name
        member = device.create(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members", data)
        if member.properties["fullPath"] != '/Common/' + member_name:
            raise Exception(member.properties["fullPath"])
        else:
            print(f"Member {member_name} created.")
##create new vs type standard
for l in appv:
    count = count + 1
    poolname = l[0]
    Descrip = l[2]
    vs_type = l[3]
    VIP_address = l[4]
    vsports = l[5]
    if vs_type == 'standard' and vs_type != '':
        virtual_name = 'vs_' + VIP_address + '_' + str(vsports)
        pvirtual_name = partition_name + 'vs_' + VIP_address + '_' + str(vsports)
        # Test if virtual server exists
        if device.exist(f"/mgmt/tm/ltm/virtual/{rest_format(pvirtual_name)}"):
            print(style.RED + f"Virtual {virtual_name} exists." + '\033[0m')
        else:
            data = {}
            data["name"] = virtual_name
            data["destination"] = VIP_address + ':' + str(vsports)
            data["description"] = Descrip
            data["ipProtocol"] = "tcp"
            data["profilesReference"] = {"items": [ {"context": "all", "name": "http"}, {"context": "all", "name": "tcp"}, {"context": "clientside", "name": "clientssl"}] }
            data["vlans"] = ["/Common/Internal_Web", "/Common/MGMT"]
            data["vlansEnabled"] = True
            data["sourceAddressTranslation"] = {"type": "none"}
            data["persist"] = "source_addr"
            data["pool"] = 'pool_' + str(vsports) + '_' + VIP_address
            data["rules"] = ["/Common/irule_Snat_Same_Vlan", "/Common/irule_for_attacker_VIP_IP_internet_v1"]
            virtual = device.create("/mgmt/tm/ltm/virtual", data)
            if virtual.properties["fullPath"] != pvirtual_name:
                raise Exception(virtual.properties["fullPath"])
            else:
                print(f"Virtual {virtual_name} created.")
#create new vs type performance(L4)
    elif vs_type == 'L4' and vs_type != '':
        virtual_name = 'vs_' + VIP_address + '_' + str(vsports)
        pvirtual_name = partition_name + 'vs_' + VIP_address + '_' + str(vsports)
        # Test if virtual server exists
        if device.exist(f"/mgmt/tm/ltm/virtual/{rest_format(pvirtual_name)}"):
            print(style.RED + f"Virtual {virtual_name} exists." + '\033[0m')
        else:
            data = {}
            data["name"] = virtual_name
            data["destination"] = VIP_address + ':' + str(vsports)
            data["description"] = Descrip
            data["ipProtocol"] = "tcp"
            data["profilesReference"] = {"items": [ {"context": "all", "name": "fastL4"} ] }
            data["vlans"] = ["/Common/Internal_Web", "/Common/MGMT"]
            data["vlansEnabled"] = True
            data["sourceAddressTranslation"] = {"type": "automap"}
            data["persist"] = "source_addr"
            data["pool"] = 'pool_' + str(vsports) + '_' + VIP_address
            data["rules"] = ["/Common/irule_Snat_Same_Vlan", "/Common/irule_for_attacker_VIP_IP_internet_v1"]
            virtual = device.create("/mgmt/tm/ltm/virtual", data)
            if virtual.properties["fullPath"] != pvirtual_name:
                raise Exception(virtual.properties["fullPath"])
            else:
                print(f"Virtual {virtual_name} created.")
    else:
        continue
#    }
#save_config = requests.post(url = save_config_url,headers = creat_header,data = json.dumps(save_config_pyload),verify = False)
print("建立設定並存檔完畢")
print("\nEnd Job")
