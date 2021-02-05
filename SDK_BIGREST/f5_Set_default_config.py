#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       f5_Set_default_config.py
#
#        USAGE: f5_Set_default_config.py
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
#      Created Time: 2021-01-29 17:14:49
#      Last modified: 2021-01-29 17:14
#     REVISION: ---
#===============================================================================


settings = br.load('/mgmt/tm/sys/dns')[0]
settings.properties['nameServers'] = ['8.8.8.8']
settings = br.save(settings)
