#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       Grafana_v2.dashboard.py
#
#        USAGE: Grafana_v2.dashboard.py
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
#      Created Time: 2021-01-25 16:36:36
#      Last modified: 2021-01-25 16:36
#     REVISION: ---
#===============================================================================
#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from grafanalib import core


def _annotations(name):
    return core.Annotations(list=[{
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": True,
        "hide": True,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": name,
        "type": "dashboard"
    }])


def _row(title):
    return core.Row(panels=[
        core.Graph(
            title=title,
            dataSource='prometheus',
            targets=[
                core.Target(
                    expr=title,
                    legendFormat='{{namespace}}',
                ),
            ],
            yAxes=[
                core.YAxis(format=core.NO_FORMAT),
                core.YAxis(format=core.SHORT_FORMAT),
            ]
        )
    ])


dashboard = core.Dashboard(
    title='hogehoge',
    uid="XK5tCdAWk",
    annotations=_annotations('Annotations & Alerts'),
    rows=[
        _row('title')
    ],
).auto_panel_ids()
