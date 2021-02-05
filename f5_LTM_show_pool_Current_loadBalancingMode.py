#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_LTM_show_pool_Current_loadBalancingMode.py
#
#        USAGE: f5_LTM_show_pool_Current_loadBalancingMode.py
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
#      Created Time: 2021-01-22 08:33:44
#      Last modified: 2021-01-22 08:34
#     REVISION: ---
#===============================================================================
#!/usr/bin/env python
####
#
#
#
#
from f5.bigip import ManagementRoot
import getpass
import time
import sys

#
host = input("F5_host_IP: ")
username = input("F5_username: ")
password = getpass.getpass('F5_Password: ')
#
dtf = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
path = ("%s_LTM_LB_Mode_%s.txt" % (dtf, host))

te = open(path,'a+')  # File where you need to keep the logs

class Unbuffered:

   def __init__(self, stream):

       self.stream = stream

   def write(self, data):

       self.stream.write(data)
       self.stream.flush()
       te.write(data)    # Write the data of stdout here to a text file as well

   def flush(self):
        pass

sys.stdout=Unbuffered(sys.stdout)

mgmt = ManagementRoot(host, username, password)
#
print("\n")
all_pool = mgmt.tm.ltm.pools.get_collection()
for pool in all_pool:
    print("pool_name: %s \tCurrent_loadBalancingMode:\t %s " % (pool.name, pool.loadBalancingMode))

