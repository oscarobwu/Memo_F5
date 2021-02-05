#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_mirrio_check_v1.py
#
#        USAGE: f5_mirrio_check_v1.py
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
#      Created Time: 2021-01-05 09:59:17
#      Last modified: 2021-01-05 10:14
#     REVISION: ---
#===============================================================================
import getpass
import os
import tempfile
import time
#
from csv import DictReader
from f5.bigip import ManagementRoot
print('輸入帳號_Please enter credentials to login into Load Balancer -' + '\r')
f5user = input('Username: ')
f5pw = getpass.getpass('Password: ')
with open('MirrorCheck.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        f5host = row['F5_Host_IP']
        f5name = row['F5_Host_Name']
        print('Logging on ' + str(f5host))
        try:
            if(f5host == 'break'):
                sys.exit()
            mgmt = ManagementRoot(f5host, f5user, f5pw)
            #
            x = mgmt.tm.util.bash.exec_cmd('run', utilCmdArgs='-c "tmsh list ltm virtual one-line | grep -e \'mirror enabled\|context clientside\' "')
            f5raw = x.raw
            #
            print(f5raw)
            if 'commandResult' in f5raw.keys():
                print( "blah-login suss")
                line = x.commandResult
                filename = 'guess_my_name.%s.txt' % os.getpid()
                ftemp = open(filename, 'w')
                ftemp.write( line )
                print( 'temp.name:', ftemp.name)
                #print(line)
                #
                ftemp.close()
                #
                f = open(filename, 'r')
                m = open(f5host + '_ssl_mirror.txt', 'w')
                mirror_words = f.readlines()
                #
                for ln in mirror_words:
                    if "mirror enabled" in ln and "context clientside" in ln:
                        m.write(ln)
                #
                f.close()
                os.remove(filename)
            else:
                #print "boo"
                continue
        except:
            print('Login failed! ')
