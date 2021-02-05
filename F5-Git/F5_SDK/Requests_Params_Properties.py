#########################################################################
# title: Requests_Params_Properties.py                                  #
# author: Dario Garrido                                                 #
# date: 20200410                                                        #
# description: Example of using request_params with properties          #
#########################################################################

from f5.bigip import ManagementRoot

# ----------------------------------------------------------

session = ManagementRoot("F5_mgmt_IP","username","password",token=True)

virtuals = session.tm.ltm.virtuals.get_collection(requests_params={'params': '$select=name,destination'})
# https:// <F5_mgmt_IP>/mgmt/tm/ltm/virtual?$select=name,destination
for virtual in virtuals:
	print("VS Name: {}".format(virtual['name']))
	print("VS Destination: {}".format(virtual['destination']))

# ----------------------------------------------------------
