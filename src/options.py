# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import traceback
from src import log, soap_api

try:
    from src import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    log.userMessage.error(e)
    sys.exit(-1)

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
        try:
            ci = soap_api.get('cmdb_ci', {'name': ci_name})
            log.userMessage.debug('Got CI inside filter_ci():\n%s' %
                                  str(ci).split(':', 1)[1].split(' ', 1)[1])
        except:
            log.userMessage.warning("Couldn\'t get CI \"%s\" from Service Now. \
Skipping filter_ci()." % ci_name)
            log.userMessage.debug(traceback.format_exc())
            return True

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
    try:
        response = soap_api.get('incident', data)
        log.userMessage.info('Requested incident: %s' %
                             str(response).split(':', 1)[1].split(' ', 1)[1])
    except:
        log.userMessage.error("Error getting incident from Service Now.")
        log.userMessage.debug("Incident: %s" % incident_number)
        log.userMessage.debug(traceback.format_exc())


def handle_get_alert_event(alert_event_number):
    data = {
        'number': alert_event_number
    }
    try:
        response = soap_api.get('u_alert_event', data)
        log.userMessage.info('Requested alert event: %s' %
                             str(response).split(':', 1)[1].split(' ', 1)[1])
    except:
        log.userMessage.error("Error getting alert event from Service Now.")
        log.userMessage.debug("Alert event: %s" % alert_event_number)
        log.userMessage.debug(traceback.format_exc())


def handle_get_ci(ci_name):
    data = {
        'name': ci_name
    }
    try:
        response = soap_api.get('cmdb_ci', data)
        log.userMessage.info('Requested CI: %s' %
                             str(response).split(':', 1)[1].split(' ', 1)[1])
    except:
        log.userMessage.error("Error getting CI from Service Now.")
        log.userMessage.debug("CI: %s" % ci_name)
        log.userMessage.debug(traceback.format_exc())


def handle_insert_incident(parameters):
    data = parse_parameters(parameters)
    try:
        response = soap_api.insert('incident', data)
        log.userMessage.info('Incident inserted: %s' %
                             str(response).split(':', 1)[1].split(' ', 1)[1])
    except:
        log.userMessage.error("Error inserting incident to Service Now.")
        log.userMessage.debug("Incident: %s" % data)
        log.userMessage.debug(traceback.format_exc())


def handle_insert_alert_event(parameters):
    data = parse_parameters(parameters)
    if (filter_alert_event(data) and filter_ci(data['cmdb_ci'])):
        try:
            response = soap_api.insert('u_alert_event', data)
            log.userMessage.info(
                'Alert event inserted: %s' %
                str(response).split(':', 1)[1].split(' ', 1)[1]
            )
        except Exception, e:
            log.userMessage.error("Error inserting alert event to \
Service Now: %s" % e)
            log.alertEventsNotInserted.info(data)
            log.userMessage.debug(traceback.format_exc())
    else:
        log.userMessage.info("Event ignored according to configured match \
conditions.")


def handle_insert_ci(parameters):
    log.userMessage.info("Insert CI option yet not implemented.")


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
