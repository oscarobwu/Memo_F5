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
#      Last modified: 2021-02-01 10:13
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
from netaddr import IPNetwork, IPAddress
# Internal imports
# Import only with "from x import y", to simplify the code.
from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token

#
p = Pinyin()
urllib3.disable_warnings()   #disable ssl warning

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
            print(f"monitor {monic_name} exists.")
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
#        if vip_port == '80' or vip_port == '443':
#            moni_name = 'http'
#        else:
#            moni_name = 'TCP_' + str(vip_port)
#
        pool_names = 'pool_' + str(vip_port) + '_' + vip_addr
        if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_names)}"):
            print(f"Pool {pool_names} exists.")
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
#        pool_url = 'https://%s/mgmt/tm/ltm/pool/' %(f5_ip)
#        desc = p.get_pinyin(Descrip)
#        pool_name = ("pool_{}_{}".format(vip_port, vip_addr))
#        print("創建的pool : ",pool_name)
#        creat_pool_data = {
#            'partition':'Common',
#            'name':pool_name,
#            'description':desc,
#            'monitor':moni_name
#            }
#        pool = requests.post(url = pool_url,headers = creat_header, data = json.dumps(creat_pool_data),verify = False)
    else :
        continue

print("\nAdd Pool member\n")
##members into pool
partition_name = "/Common/"
pool_name_last = []
for l in appv:
    count = count + 1
    poolname = l[0]
    vip_addr = l[4]
    vip_port = l[5]
    Descrip = l[2]
    pmb_ip = l[6]
    pmb_port = l[7]
    #time.sleep(1)
    #pool_name_last = pool_name
    #pool_name_last = []
    #pool_name_last = p.get_pinyin("pool_{}_{}".format(vip_port, vip_addr))
    #print(pool_name_last)
    name_to_py = p.get_pinyin("pool_{}_{}".format(vip_port, vip_addr))
    if vip_addr == '':
        #pool_name = pool_name_last
        pool_name = pool_name_last[-1:][0]
        #pool_name = a
    else:
        #pool_name = ("pool_{}_{}".format(vip_port, vip_addr))
        pool_name = "pool_{}_{}".format(vip_port, vip_addr)
        pool_name_last.append("pool_%s_%s" % (vip_port, vip_addr))
        time.sleep(1)
    #pool_member_name = 'node_' + pmb_ip
    #pool_member_ip = pmb_ip
    #pool_member_port = pmb_port
    member_name = 'node_' + pmb_ip + ':' + str(pmb_port)
    pmember_name = partition_name + 'node_' + pmb_ip + ':' + str(pmb_port)
    # Test if poolmember not exists
    print(pool_name)
    if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(pmember_name)}"):
        print(f"poolmember {member_name} in {pool_name} exists.")
    else:
        #raise Exception(f"Creat poolmemeber {member_name} in {pool_name}.")
        data = {}
        data["name"] = member_name
        member = device.create(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members", data)
        if member.properties["fullPath"] != '/Common/' + member_name:
            raise Exception(member.properties["fullPath"])
        else:
            print(f"Member {member_name} created.")
#    pool_member_url = 'https://%s/mgmt/tm/ltm/pool/%s/members' %(f5_ip,pool_name)
#    member_into_pool_data = {
#        'partition':'Common',
#        'name':'%s:%s' % (pool_member_name,pool_member_port),'address':pool_member_ip
#        }
#    pool = requests.post(url = pool_member_url,headers = creat_header, data = json.dumps(member_into_pool_data),verify = False)
#    print("pool: {} Add Poolmember : {}".format(pool_name, pool_member_ip))
##
##create new vs type standard
#vs_url = 'https://%s/mgmt/tm/ltm/virtual/' %(f5_ip)
#for l in appv:
#    count = count + 1
#    poolname = l[0]
#    Descrip = l[2]
#    vs_type = l[3]
#    vip_addr = l[4]
#    vip_port = l[5]
#    if vs_type == 'standard' and vs_type != '':
#        name_to_py = p.get_pinyin("%s" % poolname)
#        vs_name = "vs_{}_{}".format(vip_addr, vip_port)
#        print("創建的VS : ",vs_name,"類型:standard")
#        vs_ip = vip_addr
#        vs_port = vip_port
#        desc = p.get_pinyin("vs_{}_{}_{}".format(vip_addr, vip_port, poolname))
#        pool_name = "pool_{}_{}".format(vip_port, vip_addr)
#        create_vs_data = {
#            'partition':'Common',
#            'name':vs_name,
#            'description':desc,
#            'destination':'%s:%s' %(vs_ip,vs_port),
#            'pool':pool_name,
#            'profiles': [
#                {'name':'tcp'},
#                {'name':'http'}
#                ]
#            }
#        create_vs = requests.post(url = vs_url,headers = creat_header,data = json.dumps(create_vs_data),verify = False)
##create new vs type performance(L4)
#    elif vs_type == 'L4' and vs_type != '':
#        vs_url = 'https://%s/mgmt/tm/ltm/virtual/' %(f5_ip)
#        name_to_py = p.get_pinyin("%s" %poolname)
#        vs_name = "vs_{}_{}".format(vip_addr, vip_port)
#        print("創建的VS : ",vs_name,"類型:L4")
#        vs_ip = vip_addr
#        vs_port = vip_port
#        desc = p.get_pinyin("vs_{}_{}_{}".format(vip_addr, vip_port, poolname))
#        pool_name = "pool_{}_{}".format(vip_port, vip_addr)
#        create_vs_data = {
#            'partition':'Common',
#            'name':vs_name,
#            'description':desc,
#            'ipProtocol':'tcp',
#            'destination':'%s:%s' %(vs_ip,vs_port),
#            'pool':pool_name,
#            'profiles': [
#                {'name':'fastL4'}
#                ]
#            }
#        create_vs = requests.post(url = vs_url,headers = creat_header,data = json.dumps(create_vs_data),verify = False)
#    else:
#        continue
#
##save config
#save_config_url = 'https://%s/mgmt/tm/sys/config/' %(f5_ip)
#save_config_pyload = {
#    'partition':'Common',
#    'command':'save'
#    }
#save_config = requests.post(url = save_config_url,headers = creat_header,data = json.dumps(save_config_pyload),verify = False)
print("建立設定並存檔完畢")
print("\nEnd Job")
