#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       test_dic.py
#
#        USAGE: test_dic.py
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
#      Created Time: 2021-01-28 12:19:32
#      Last modified: 2021-01-28 12:55
#     REVISION: ---
#===============================================================================
import pandas as pd


F5_list = [
 {'Numb': '001', 'F5_host_IP': '172.16.14.166', 'F5_host_Name': 'F5-BT-VE-02.localdomain', 'F5_host_Location': 'DC01', 'F5_host_vip_subnet': '172.19.99.0/24 172.19.33.0/24'},
 {'Numb': '002', 'F5_host_IP': '172.16.14.167', 'F5_host_Name': 'F5-BT-VE-03.localdomain', 'F5_host_Location': 'DC03', 'F5_host_vip_subnet': '172.19.98.0/24 172.19.34.0/24'},
 {'Numb': '003', 'F5_host_IP': '172.16.14.168', 'F5_host_Name': 'F5-BT-VE-04.localdomain', 'F5_host_Location': 'DC05', 'F5_host_vip_subnet': '172.19.97.0/24 172.19.35.0/24'}]


x = pd.DataFrame.from_dict(F5_list, orient='columns')

print(x)

f5h = pd.DataFrame(x, columns=['F5_host_IP', 'F5_host_vip_subnet'])
f5host = f5h.values

for y in f5host:
    #
    t = y[1]
    print(t)
