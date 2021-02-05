#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       BIG_IP_set_pool_members_v1.py
#
#        USAGE: BIG_IP_set_pool_members_v1.py
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
#      Created Time: 2021-01-15 08:53:15
#      Last modified: 2021-01-15 08:57
#     REVISION: ---
#===============================================================================
from f5.bigip import ManagementRoot
import argparse
import logging

STATES = ['enabled', 'disabled', 'forced_offline', 'checked']

description = 'enables, disables and forces offline f5 pools members'
parser = argparse.ArgumentParser(description=description)

parser.add_argument('-H', '--bigip', required=True, type=str,
                    help='BIPIP to work with')
parser.add_argument('-U', '--username', required=True, type=str,
                    help='USERNAME to work with')
parser.add_argument('-P', '--passwd', required=True, type=str,
                    help='PASSWORD to work with')
parser.add_argument('-p', '--pool', required=True, type=str,
                    help='pool to work with')
parser.add_argument('-n', '--poolmember', required=True, type=str,
                    help='poolmember to work with')
parser.add_argument('-s', '--state', required=True, choices=STATES,
                    help='pool to work with')
parser.add_argument('-r', '--readonly', dest='readonly',
                    action='store_true',
                    help='readonly mode for debug (default disabled)')

cli_options = parser.parse_args()
FORMAT = '%(asctime)s %(levelname)s %(module)s %(message)s'
logging.basicConfig(format=FORMAT, level='INFO')
logger = logging.getLogger('set_pool_members_state')
host_ip = cli_options.bigip
host_user = cli_options.username
host_passwd = cli_options.passwd

#mgmt = ManagementRoot(host_ip, "op", "opop")
mgmt = ManagementRoot(host_ip, host_user, host_passwd)
pool = mgmt.tm.ltm.pools.pool.load(name=cli_options.pool, partition='Common')

#poolmember = pool.members_s.get_collection()dd

m1 = pool.members_s.members.load(partition='Common', name=cli_options.poolmember)

fail = mgmt.tm.sys.failover.load()
failOverStat = fail.apiRawValues['apiAnonymous'].rstrip()
#print ("%s: Ver %s, %s" % (host_ip, mgmt.tmos_version, failOverStat))
#print ("%s" % ( failOverStat))
fields = failOverStat.strip().split()
aabbcc = fields[1]
print( aabbcc )

if aabbcc in ["active"]:
        #print ( denow )
        #for member in pool.members_s.get_collection():
        for member in [m1]:
                logger.info('%s: %s %s' % (member.name, member.session, member.state))
                if cli_options.state == 'enabled':
                        # enables member
                        logger.info('enables member %s, previous state: %s' %
                                                (member.name, member.state))
                        member.state = 'user-up'
                        member.session = 'user-enabled'
                elif cli_options.state == 'disabled':
                        # disables member
                        logger.info('disables member %s, previous state: %s' %
                                                (member.name, member.state))
                        member.session = 'user-disabled'
                elif cli_options.state == 'forced_offline':
                        # forces online member
                        logger.info('forces online member %s, previous state: %s' %
                                                (member.name, member.state))
                        member.state = 'user-down'
                        member.session = 'user-disabled'
                elif cli_options.state == 'checked':
                        # Checl online member
                        stt = member.session
                        logger.info('checked online member %s, previous state: %s' %
                                                (member.name, member.state))
                        if "monitor-enabled" in stt:
                            logger.info('checked online member %s, previous state: %s' %(member.name, member.state))
                        else:
                            logger.info(另外一批有異常請檢查)
                        #print(False)

                if not cli_options.readonly:
                        member.update()
                else:
                        logger.info('readonly mode, no changes applied')

                logger.info('%s: %s %s' % (member.name, member.session, member.state))
else:
        print("this will do Nothing 請修改 Active F5 的 IP ")
        exit()

