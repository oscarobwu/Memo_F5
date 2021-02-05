#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       grcpu.py
#
#        USAGE: grcpu.py
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
#      Created Time: 2021-01-25 16:48:41
#      Last modified: 2021-01-25 16:52
#     REVISION: ---
#===============================================================================
from grafanalib.core import *
dashboard = core.Dashboard(
  title="InFluxDashboard",
  rows=[
    Row(panels=[
      Graph(
        title="Free Disk",
        dataSource="SystemHealth",
        targets=[
          Target(
            #expr='wmi_logical_disk_free_bytes{instance="192.168.0.6:9182",volume!~"C:"}',
            expr='SELECT mean("Percent_Idle_Time") FROM "win_cpu" WHERE ("host" = 'DESKTOP-V4S49U7') AND $timeFilter GROUP BY time(10m) fill(null)',
            legendFormat="1xx",
            refId='A',
          ),
        ],
        yAxes=single_y_axis(format=BYTES_FORMAT),
      ),
    ]),
  ],
).auto_panel_ids()
