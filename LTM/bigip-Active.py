#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       bigip-Active.py
#
#        USAGE: bigip-Active.py
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
#      Created Time: 2021-01-29 09:30:46
#      Last modified: 2021-01-29 09:36
#     REVISION: ---
#===============================================================================
#
# bigip_active: Connects to the active member of a Device Group regardless of
#   the original hostname.
__author__ = 'buzzsurfr'
__version__ = '0.1'
#  Standard Library
import sys
import itertools
#  Related Third-Party
import getpass
#  Local Application/Library Specific
import bigsuds
def bigip_active(hostname, username='admin', password='admin', debug=False, cachedir=None, verify=False, timeout=90):
#  Connect to specified BIG-IP
	b = bigsuds.BIGIP(hostname, username, password, debug, cachedir, verify, timeout)
#  Determine whether device is active
	if(b.Management.DeviceGroup.get_failover_status()['status'] != 'ACTIVE'):
		local_device = b.Management.Device.get_local_device()
		new_device = False
		for device in list(set(itertools.chain.from_iterable(b.Management.DeviceGroup.get_device(b.Management.DeviceGroup.get_list())))).remove(local_device):
			if(b.Management.Device.get_failover_state(device) == 'HA_STATE_ACTIVE'):
				new_device = device
			if(new_device):
				print b.Management.Device.get_local_device()[8:]+" is not active.  Switching to "+new_device[8:]
				b = bigsuds.BIGIP(new_device[8:], username, password, debug, cachedir, verify, timeout)
			return b

if __name__ == '__main__':
F5_Host_IP = input('F5-Host-IP :')
f5_user = input('Username: ')
bigip_active(F5_Host_IP, f5_user, getpass.getpass())
