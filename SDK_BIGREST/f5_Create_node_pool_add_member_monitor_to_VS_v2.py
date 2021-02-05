#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:      f5_Create_node_pool_add_member_v1.py 
#
#        USAGE: f5_Create_node_pool_add_member_v1.py
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
#      Created Time: 2021-01-27 09:35:46
#      Last modified: 2021-01-27 20:50
#     REVISION: ---
#===============================================================================
import getpass
import os
import hashlib
import sys

# Internal imports
# Import only with "from x import y", to simplify the code.
from bigrest.bigip import BIGIP
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import token

# Get username, password, and ip
F5_Host = input('Device IP or name: ')
print("Username: ", end="")
F5_username = input()
F5_password = getpass.getpass('Password: ')
#print("Device IP or name: ", end="")
#
partition_name = "/Common/"
#
Job_name = input('輸入單號或說明: ')
#print("Node_ip : ", end="")
#node_ip_address = input()
print('請輸入資料_IP_Address，直接按下Enter 結束 : ')
buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        buffer.append(line)
#print (buffer)
node_list = buffer

# Create a device object with basic authentication
device = BIGIP(F5_Host, F5_username, F5_password)

# Create node
for node_ip_address in node_list:
    node_name = 'node_' + node_ip_address
    if device.exist(f"/mgmt/tm/ltm/node/{rest_format(node_name)}"):
        print(f"Node {node_name} exists.")
    else:
        #raise Exception(f"Create {node_name} and Check not exists.")
        data = {}
        data["name"] = node_name
        data["address"] = node_ip_address
        data["description"] = Job_name
        node = device.create(
            f"/mgmt/tm/ltm/node/", data)
        if node.properties["fullPath"] != '/Common/' + 'node_' + node_ip_address:
            raise Exception(node.properties["fullPath"])
        else:
            print(f"Node {node_ip_address} created.")

VIP_address = input('VIP Address: ')

print('請輸入資料 port list，如 \n80\n443\n8080\n...直接按下Enter 結束 : ')
port_buffer = []
while True:
    line = sys.stdin.readline().rstrip('\n')
    if line == '':
        break
    else:
        port_buffer.append(line)
#print (buffer)
port_list = port_buffer

# Create TCP monitor to other port
for port in port_list:
    moni_name = 'TCP-' + port
    if device.exist(f"/mgmt/tm/ltm/monitor/tcp/{rest_format(moni_name)}"):
        print(f"monitor {moni_name} exists.")
    else:
        #raise Exception(f"monitor {member_name} in {pool_name}.")
        data = {}
        data["name"] = moni_name
        data["destination"] = '*.' + port
        monitor = device.create(
            f"/mgmt/tm/ltm/monitor/tcp", data)
        if monitor.properties["fullPath"] != '/Common/' + moni_name:
            raise Exception(monitor.properties["fullPath"])
        else:
            print(f"Pool {moni_name} created.")

# Create pool
for pools in port_list:
    pool_names = 'pool_' + pools + '_' + VIP_address
    if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_names)}"):
        print(f"Pool {pool_names} exists.")
    else:
        #raise Exception(f"Create {pool_names} and Check not exists.")
        if pools == '80' or pools == '443':
            monitor_name = "/Common/http"
        else:
            monitor_name = '/Common/TCP-' + pools
        data = {}
        data["name"] = pool_names
        data["description"] = Job_name
        data["monitor"] = monitor_name
        print(pool_names)
        #data["description"] = Job_name
        pool = device.create(f"/mgmt/tm/ltm/pool", data)
        if pool.properties["fullPath"] != '/Common/' + pool_names:
            raise Exception(pool.properties["fullPath"])
        else:
            print(f"Pool {pool_names} created.")


# Add pool member
for port in port_list:
    pool_name = 'pool_' + port + '_' + VIP_address
    for members in node_list:
        member_name = 'node_' + members + ':' + port
        pmember_name = partition_name + 'node_' + members + ':' + port
        # Test if poolmember not exists
        if device.exist(f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members/{rest_format(pmember_name)}"):
            print(f"poolmember {member_name} in {pool_name} exists.")
        else:
            #raise Exception(f"Creat poolmemeber {member_name} in {pool_name}.")
            data = {}
            data["name"] = member_name
            member = device.create(
                f"/mgmt/tm/ltm/pool/{rest_format(pool_name)}/members", data)
            if member.properties["fullPath"] != '/Common/' + member_name:
                raise Exception(member.properties["fullPath"])
            else:
                print(f"Member {member_name} created.")

# Add virtual server
for vsports in port_list:
    virtual_name = 'vs_' + VIP_address + '_' + vsports
    pvirtual_name = partition_name + 'vs_' + VIP_address + '_' + vsports
    # Test if virtual server exists
    if device.exist(f"/mgmt/tm/ltm/virtual/{rest_format(pvirtual_name)}"):
        print(f"Virtual {virtual_name} exists.")
    else:
        #raise Exception(f"Error testing if {virtual_name} exists.")
        #if pools == '80' or pools == '443':
        #    profile_name = {"items": [ {"context": "all", "name": "http"}, {"context": "all", "name": "tcp"}, {"context": "clientside", "name": "clientssl"}] }
        #else:
        #    profile_name = {"items": [ {"context": "all", "name": "fastL4"}, {"context": "all", "name": "tcp"} ] }
        #pf = [{'name': 'http', 'name': 'tcp'}]
        data = {}
        data["name"] = virtual_name
        data["destination"] = VIP_address + ':' + vsports
        data["description"] = Job_name
        data["ipProtocol"] = "tcp"
        if vsports == '80' or vsports == '443':
            data["profilesReference"] = {"items": [ {"context": "all", "name": "http"}, {"context": "all", "name": "tcp"}, {"context": "clientside", "name": "clientssl"}] }
        else:
            data["profilesReference"] = {"items": [ {"context": "all", "name": "fastL4"} ] }
        #data["profilesReference"] = {"items": [ {"context": "all", "name": "fastL4"} ] }
        data["vlans"] = ["/Common/Internal_Web", "/Common/MGMT"]
        data["vlansEnabled"] = True
        if vsports == '80':
            data["sourceAddressTranslation"] = {"type": "none"}
        elif vsports == "443":
            data["sourceAddressTranslation"] = {"type": "automap"}
        else:
            data["sourceAddressTranslation"] = {"pool": "/Common/testpip111", "type": "snat" }
        data["persist"] = "source_addr"
        data["pool"] = 'pool_' + vsports + '_' + VIP_address
        data["rules"] = ["/Common/irule_Snat_Same_Vlan", "/Common/irule_for_attacker_VIP_IP_internet_v1"]
        virtual = device.create("/mgmt/tm/ltm/virtual", data)
        if virtual.properties["fullPath"] != pvirtual_name:
            raise Exception(virtual.properties["fullPath"])
        else:
            print(f"Virtual {virtual_name} created.")
