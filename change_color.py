#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       change_color.py
#
#        USAGE: change_color.py
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
#      Created Time: 2021-01-06 10:41:45
#      Last modified: 2021-01-06 15:49
#     REVISION: ---
#===============================================================================
import pandas as pd
import numpy as np

# Seeding random data from numpy
np.random.seed(24)

writer = pd.read_excel('2021-01-06-15-48_vs_pool.xlsx')
# Making the DatFrame
#df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
#writer = pd.concat([writer, pd.DataFrame(np.random.randn(10, 4),
#                                 columns=list('BCDE'))], axis=1)
#writer = pd.concat([writer, pd.DataFrame(np.random.randn(10, 4),
#                                 columns=list('vs_name'))], axis=1)
writer = pd.concat([writer, pd.DataFrame(columns=list('vs_name'))], axis=1)

# DataFrame without any styling
print("Original DataFrame:\n")
#print(df)
print(writer)
print("\nModified Stlying DataFrame:")
#writer.style.set_properties(**{'background-color': 'black',
#                           'color': 'green'})
writer.style.set_properties(**{'background-color': 'black',
                           'color': 'red'})
