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
import servicenow_conf


def parse_parameters(parameters):
    data = {
        'cmdb_ci': '.'.join(parameters.split(';')[0].split('.')[0:2]),
        'u_opm_severity': parameters.split(';')[1],
        'u_opm_entity': parameters.split(';')[2],
        'short_description': ''.join(parameters.split(';')[3:])
    }
    return data


def filter_ci(ci_name):
    ''' returns False if the CI is to be ignored '''
    if (servicenow_conf.IGNORE_CI is not None):
        ci = soap_api.get('cmdb_ci', {'name': ci_name})
        for k in servicenow_conf.IGNORE_CI.keys():
            if (servicenow_conf.IGNORE_CI[k] in ci[k]):
                return False
    return True


def filter_alert_event(event):
    ''' returns False if the alert event is to be ignored '''
    if (servicenow_conf.IGNORE_ALERT_EVENT is not None):
        for k in servicenow_conf.IGNORE_ALERT_EVENT.keys():
            if (servicenow_conf.IGNORE_ALERT_EVENT[k] in event[k]):
                return False
    return True


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
    response = soap_api.insert('incident', parse_parameters(parameters))
    print response


def handle_insert_alert_event(parameters):
    data = parse_parameters(parameters)
    if (filter_alert_event(data) and filter_ci(data['cmdb_ci'])):
        response = soap_api.insert('u_alert_event', data)
        print response
    else:
        print "Event ignored according to configured match conditions."


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
