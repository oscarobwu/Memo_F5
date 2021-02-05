#!/usr/bin/python
#-*- coding: utf-8 -*-
#===============================================================================
#
#         Filename:       kube-state-metrics.dashboard.py
#
#        USAGE: kube-state-metrics.dashboard.py
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
#      Created Time: 2021-01-25 16:18:36
#      Last modified: 2021-01-25 16:33
#     REVISION: ---
#===============================================================================
from grafanalib.core import *


def resource_row(resource):
    return Row(panels=[
        Graph(
            title='Number of %s by namespace' % resource,
            dataSource='prometheus',
            targets=[
                Target(
                    expr='count(kube_%s_created) by (namespace)' % resource,
                    legendFormat='{{namespace}}',
                ),
            ],
            yAxes=[
                YAxis(format=BYTES_FORMAT),
                YAxis(format=SHORT_FORMAT),
            ]
        )
    ])


dashboard = Dashboard(
    title="grafanalib: Kubernetes resource count",
    rows=[
        resource_row('deployment'),
        resource_row('daemonset'),
        resource_row('job'),
        resource_row('cronjob'),
        resource_row('pod'),
        resource_row('configmap'),
        resource_row('secret'),
        resource_row('service'),
        resource_row('endpoint'),
    ],
).auto_panel_ids()
