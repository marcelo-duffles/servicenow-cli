# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

try:
    from lib import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    print e
    sys.exit(-1)

import soap_api


def handle_get_incident(incident_number):
    data = {
        'number': incident_number
    }
    response = soap_api.get('incident', data)
    print response


def handle_get_alert_event(alert_event_number):
    data = {
        'number': alert_event_number
    }
    response = soap_api.get('u_alert_event', data)
    print response


def handle_get_ci(ci_name):
    data = {
        'name': ci_name
    }
    response = soap_api.get('cmdb_ci',data)
    print response


def handle_insert_incident(parameters):

    data = {
        'cmdb_ci': '.'.join(parameters.split(';')[0].split('.')[0:2]),
        'u_opm_severity': parameters.split(';')[1],
        'u_opm_entity': parameters.split(';')[2],
        'short_description': ''.join(parameters.split(';')[3:])
    }
    response = soap_api.insert('incident', data)
    print response


def handle_insert_alert_event(parameters):

    data = {
        'cmdb_ci': '.'.join(parameters.split(';')[0].split('.')[0:2]),
        'u_opm_severity': parameters.split(';')[1],
        'u_opm_entity': parameters.split(';')[2],
        'short_description': ''.join(parameters.split(';')[3:])
    }
    response = soap_api.insert('u_alert_event', data)
    print response


def handle_insert_ci(parameters):
    print "Insert CI option yet not implemented."


insert_options = {
    'incident': handle_insert_incident,
    'alert_event': handle_insert_alert_event,
    'ci': handle_insert_ci,
}

get_options = {
    'incident': handle_get_incident,
    'alert_event': handle_get_alert_event,
    'ci': handle_get_ci,
}

options = {
    'insert': insert_options,
    'get': get_options
}
