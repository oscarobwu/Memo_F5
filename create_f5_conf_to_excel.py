#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       create_f5_conf_to_excel.py
#
#        USAGE: create_f5_conf_to_excel.py
#
#  DESCRIPTION:f5_將VS_Pool_member寫入到excel_v1.py
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Oscarob Wu(oscarobwu@gmail.com),
# ORGANIZATION:
#      VERSION: 1.0
#      Created Time: 2021-01-05 09:05:32
#      Last modified: 2021-01-06 14:13
#     REVISION: ---
#===============================================================================
# 顯是 virtual server 和pool 和 poolmemeber
# 將檔案存到excel
import pandas as pd
import openpyxl
import datetime
import time
from f5.bigip import ManagementRoot
import datetime
import time
import getpass
import operator
#
f5_host = input('F5_mgmt_IP: ')
#f5_host = '192.168.8.168'
print("登入 主機 : %s" % f5_host)
f5_user = input('\nUsername: ')
f5_pw = getpass.getpass('\nPassword: ')
#
findword = input('\n需要搜尋比對字串: ')
#
#print("登入 主機 : %s" % f5_host)
datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M");
#mgmt = ManagementRoot('hostname', 'username', 'password')
mgmt = ManagementRoot(f5_host, f5_user, f5_pw)

# CSV header
#print('Partition, VS Name, Pool Name, Pool Members')

#df_list = pd.DataFrame()
df_list = pd.DataFrame(columns=['vs_part',
                                'vs_name',
                                'vs_ip_addr',
                                'vs_ip_port',
                                'vs_pool',
                                'Pool_memb',
                                'Pool_memb_addr'])

for virtual in mgmt.tm.ltm.virtuals.get_collection():
    # Does the virtual server have a pool assigned?
    if not getattr(virtual, 'pool', None):
        # No - print virtual server name and move on
        vs_ip_addr = virtual.destination.split('/')[2]
        vs_ip_port = virtual.destination.split(':')[1]
        #print('{},{},,'.format(virtual.partition, virtual.name))
        df_list = df_list.append({'vs_part': virtual.partition,
                                  'vs_name': virtual.name,
                                  'vs_ip_addr': vs_ip_addr,
                                  'vs_ip_port': vs_ip_port,
                                  },
                     ignore_index=True)
        continue

    # Pool partition
    vs_ip_addr = virtual.destination.split('/')[2]
    vs_ip_port = virtual.destination.split(':')[1]
    #print(virtual.destination)
    #print(vs_ip_addr)
    #print(vs_ip_port)
    # Pool partition
    pool_part = virtual.pool.split('/')[1]
    # Pool name
    pool_name = virtual.pool.split('/')[2]

    pool = mgmt.tm.ltm.pools.pool.load(
        partition=pool_part,
        name=pool_name,
    )

    members = pool.members_s.get_collection()

    # Loop to output the results however you'd like
    # Example is CSV with pool members delimited by semicolon

    # Gather members in list - makes printing easier
    pool_members = []
    pool_members_addr = []
    for member in members:
        pool_members.append(member.name)
        pool_members_addr.append(member.address)

    df_list = df_list.append({'vs_part': virtual.partition,
                              'vs_name': virtual.name,
                              'vs_ip_addr': vs_ip_addr,
                              'vs_ip_port': vs_ip_port,
                              'vs_pool': pool.name,
                              'Pool_memb': '{}'.format('\r\n'.join(pool_members)),
                              'Pool_memb_addr': '{}'.format('\r\n'.join(pool_members_addr))},
                 ignore_index=True)

print("等待最後輸出\n")
time.sleep(3)
print(df_list)
df_list.to_excel(datestring + '_vs_pool.xlsx', sheet_name=f5_host)
#
#styled = (df_list.style
#            .applymap(lambda v: 'background-color: %s' % 'green' if v=='10.99.0.14' else ''))
#
#styled = (df_list.style
#             .applymap(lambda v: 'background-color: %s' % 'green' if operator.contains(str(v), "10.99.0.14") else ''))
#styled = (df_list.style
#             .applymap(lambda v: 'background-color: %s' % 'green' if operator.contains(str(v), "809") else ''))
green = 'green'
red = 'red'
if findword:
    styled = (df_list.style
			  .applymap(lambda v: 'color: %s' % 'red' if operator.contains(str(v), findword) else ''))
    styled.to_excel(datestring + '_vs_pool.xlsx', sheet_name=f5_host, engine='openpyxl')
else:
        print("No inupnt Findword")
