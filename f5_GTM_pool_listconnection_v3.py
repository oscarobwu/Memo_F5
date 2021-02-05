#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_GTM_pool_listconnection_v3.py
#
#        USAGE: f5_GTM_pool_listconnection_v3.py
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
#      Created Time: 2021-01-22 08:31:10
#      Last modified: 2021-01-22 08:31
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import getpass
import sys
import json
import time

F5_host = input("F5-Host : ")
F5_user = input("User : ")
F5_password = getpass.getpass("F5 User password?")
#
dtf = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
path = ("%s_GTM_IP_LB_Mode_%s.txt" % (dtf, F5_host))

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
#
mgmt = ManagementRoot(F5_host, F5_user, F5_password)

# CSV header
#print('Partition, VS Name, Pool Name, Pool Members')
count = 1

#for virtual in mgmt.tm.gtm.wideips.WideipOrganizingCollection.get_collection():
wip = mgmt.tm.gtm.wideips.a_s.get_collection()
for virtual in wip:
    print ("\n{}. WideIP : {} ".format(count, virtual.name))
    count = count + 1
    #poolcheck = virtual.pools
    #if 'name' in poolcheck:
    #
    if hasattr(virtual, 'pools'):
        dic_wor1 = virtual.pools[0]
        gtmpool = dic_wor1['name']
        widlb = virtual.poolLbMode
        print ("    Pool: {}, LB = {}".format(gtmpool,widlb))
        my_pool = mgmt.tm.gtm.pools.a_s.get_collection()
        rmy_pool = mgmt.tm.gtm.pools.a_s.a.load(partition='Common', name=gtmpool)
        lb_my_pool = rmy_pool.loadBalancingMode
        my_pool_mbrs = rmy_pool.members_s.get_collection()
        print ("    Poolmember_LB: {}".format(lb_my_pool))
        for pool_mbr in my_pool_mbrs:
            #print(pool_mbr)
            mbr_name = pool_mbr.name
            #
            mbr_stats = Stats(pool_mbr.stats.load())
            mbr_desc = mbr_stats.stat.status_availabilityState['description']
            print("    \tDC_vs_name: {}, Status = {}".format(mbr_name,mbr_desc))
    else:
        print ("GTM pool not exist")

