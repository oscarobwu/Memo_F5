#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       test_check_ip.py
#
#        USAGE: test_check_ip.py
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
#      Created Time: 2021-01-28 18:18:47
#      Last modified: 2021-01-28 18:59
#     REVISION: ---
#===============================================================================
import re
import os

os.system("")

# Group of ***different*** functions for different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[42m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.YELLOW + "Hello, World!" + '\033[0m')

ipv=input("Enter an ip address : ")
a=ipv.split('.')
s=str(bin(int(a[0]))+bin(int(a[1]))+bin(int(a[2]))+bin(int(a[3])))
s=s.replace("0b",".")
m=re.search('\.[0,1]{1,8}\.[0,1]{1,8}\.[0,1]{1,8}\.[0,1]{1,8}$',s)
if m is not None:
    print(style.GREEN + "Valid sequence of input" + '\033[0m')
else :
    print(style.RED + "Invalid input sequence" + '\033[0m')

print("End Job Good Bye!!!")
