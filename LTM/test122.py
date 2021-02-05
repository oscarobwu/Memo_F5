#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       test122.py
#
#        USAGE: test122.py
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
#      Created Time: 2021-01-20 12:37:39
#      Last modified: 2021-01-20 12:38
#     REVISION: ---
#===============================================================================
import sys
import time
node = input('Node_清單使用,分隔_10.99.0.11,10.99.0.12,10.99.0.13\nIPaddress: ')
member_list = node.split(',')

print(member_list)
