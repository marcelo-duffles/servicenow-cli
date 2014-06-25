# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import traceback
import json
import time
from src import log, soap_api

try:
    from src import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    log.userMessage.error(e)
    sys.exit(-1)

import servicenow_conf


def filter_ci(ci_name):
    ''' returns False if the CI is to be ignored '''

    if (servicenow_conf.IGNORE_CI is not None):
        try:
            ci = soap_api.get('cmdb_ci', {'name': ci_name})
            log.userMessage.debug('filter_ci(): got CI %s' % ci)
        except:
            log.userMessage.warning("filter_ci(): couldn\'t get CI \"%s\" from \
Service Now, so it isn\'t possible to determine whether it matches with \
configured filtering conditions." % ci_name)
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
        log.userMessage.info('Requested incident: %s' % response)
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
        log.userMessage.info('Requested alert event: %s' % response)
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
        log.userMessage.info('Requested CI: %s' % response)
    except:
        log.userMessage.error("Error getting CI from Service Now.")
        log.userMessage.debug("CI: %s" % ci_name)
        log.userMessage.debug(traceback.format_exc())


def handle_insert_incident(parameters):
    data = servicenow_conf.build_incident(parameters)
    log.userMessage.debug("Incident built: %s" % data)
    try:
        response = soap_api.insert('incident', data)
        log.userMessage.info('Incident inserted: %s' % response)
    except:
        log.userMessage.error("Error inserting incident to Service Now.")
        log.userMessage.debug(traceback.format_exc())


def handle_insert_alert_event(parameters):
    data = servicenow_conf.build_alert_event(parameters)
    log.userMessage.debug("Alert event built: %s" % data)
    if (filter_alert_event(data) and filter_ci(data['cmdb_ci'])):
        try:
            response = soap_api.insert('u_alert_event', data)
            log.userMessage.info('Alert event inserted: %s' % response)
        except Exception, e:
            log.userMessage.error("Error inserting alert event to \
Service Now: %s" % e)
            if os.path.exists(servicenow_conf.ALERT_EVENTS_LOCK):
                log.alertEventsNotInsertedTemp.info(json.dumps(data))
            else:
                log.alertEventsNotInserted.info(json.dumps(data))
            log.userMessage.debug(traceback.format_exc())
    else:
        log.userMessage.info("Event ignored according to configured match \
conditions.")


def handle_insert_ci(parameters):
    log.userMessage.info("Insert CI option yet not implemented.")


def handle_reinsert_alert_event():
    if os.path.exists(servicenow_conf.ALERT_EVENTS_REINSERTION_LOCK):
        log.userMessage.info(
            'Aborting, because the file %s already exists, and hence another \
reinsertion is already in place.' %
            servicenow_conf.ALERT_EVENTS_REINSERTION_LOCK)
        sys.exit(0)

    # When the lock file ALERT_EVENT_REINSERTION_LOCK exists, other processes
    # can't simultaneously start another reinsertion process
    reinsertion_lock_file = open(servicenow_conf.ALERT_EVENTS_REINSERTION_LOCK,
                                 'w')
    reinsertion_lock_file.close()
    log.userMessage.debug('ALERT_EVENTS_REINSERTION_LOCK acquired.')

    # When the ALERT_EVENTS_LOCK file exists, other processes know that they
    # have to write temporarily to the temp file
    events_lock_file = open(servicenow_conf.ALERT_EVENTS_LOCK, 'w')
    events_lock_file.close()
    log.userMessage.debug('ALERT_EVENTS_LOCK acquired.')

    log.userMessage.info('Waiting 10s for the completion of ongoing writes to \
the primary file...')
    time.sleep(10)
    PRIMARY_FILENAME = log.logging_conf_dict['handlers'][
        'alertEventsNotInsertedHandler']['filename']
    primary_file = open(PRIMARY_FILENAME, 'r')

    for line in primary_file:
        originalTime = ' '.join(line.split(' ', 2)[0:2])
        data = json.loads(line.split(' ', 2)[2].rstrip('\n'))
        log.userMessage.debug("Alert event read from log file: %s %s" %
                              (originalTime, data))
        data['description'] = "Event originally generated at %s. \
It hasn\'t been inserted earlier due to an error with Service Now \
API call." % originalTime
        try:
            response = soap_api.insert('u_alert_event', data)
            log.userMessage.info('Alert event reinserted: %s' % response)
        except Exception, e:
            log.userMessage.error("Error reinserting alert event to \
Service Now: %s" % e)
            log.pastAlertEventsTemp.info(line.rstrip('\n'))
            log.userMessage.debug(traceback.format_exc())

    primary_file.close()

    # At this point, the primary file can be removed, since we have already
    # reinserted all of its events
    os.remove(PRIMARY_FILENAME)
    log.userMessage.debug('Primary alert events log file removed.')

    # When the ALERT_EVENTS_LOCK file is removed, other processes
    # know that they have to  write back to the primary file, rather than
    # continuing to write to the temp file
    os.remove(servicenow_conf.ALERT_EVENTS_LOCK)
    log.userMessage.debug('ALERT_EVENTS_LOCK released.')

    log.userMessage.info('Waiting 10s for the completion of ongoing writes to \
temp file...')
    time.sleep(10)
    TEMP_FILENAME = log.logging_conf_dict['handlers'][
        'alertEventsNotInsertedTempHandler']['filename']
    temp_file = open(TEMP_FILENAME, 'r')

    # Copying temporary alert events to the primary file...
    primary_file = open(PRIMARY_FILENAME, 'a')
    for line in temp_file:
        primary_file.write(line)
    primary_file.close()

    temp_file.close()
    os.remove(TEMP_FILENAME)
    log.userMessage.debug('Temporary alert events log file removed.')

    # When the alertEventsReinsertion lock file is removed, other processes are
    # free to start another reinsertion
    os.remove(servicenow_conf.ALERT_EVENTS_REINSERTION_LOCK)
    log.userMessage.debug('ALERT_EVENTS_REINSERTION_LOCK released.')


def handle_reinsert_incident():
    log.userMessage.info("Reinsert incident option yet not implemented.")


def handle_reinsert_ci():
    log.userMessage.info("Reinsert CI option yet not implemented.")


options = {
    'insert': {
        'incident': handle_insert_incident,
        'alert_event': handle_insert_alert_event,
        'ci': handle_insert_ci,
    },
    'reinsert': {
        'incident': handle_reinsert_incident,
        'alert_event': handle_reinsert_alert_event,
        'ci': handle_reinsert_ci,
    },
    'get': {
        'incident': handle_get_incident,
        'alert_event': handle_get_alert_event,
        'ci': handle_get_ci,
    }
}
