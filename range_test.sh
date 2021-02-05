#!/bin/sh
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       range_test.sh
#
#        USAGE: range_test.sh
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
#      Created Time: 2021-01-08 18:49:37
#      Last modified: 2021-01-08 19:03
#     REVISION: ---
#===============================================================================
for x, y, z in zip(range(1,4), range(4,7), range(7,10)):
    print(x, y, z)
