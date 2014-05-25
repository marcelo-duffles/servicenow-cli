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
    session = soap_api.build_session('incident')
    response = session.get(
        sys_id = session.getKeys(
            number=incident_number).sys_id
    )
    print response


def handle_get_ci(ci_name):
    session = soap_api.build_session('cmdb_ci')
    response = session.get(
        sys_id = session.getKeys(
            name=ci_name).sys_id
    )
    print response


def handle_insert_incident(parameters):
    session = soap_api.build_session('incident')
    """ See https://yourinstance.service-now.com/incident.do?WSDL """
    """ for available values """
    response = session.insert(
        cmdb_ci='.'.join(parameters.split()[0].split('.')[0:2]),
        opm_severity=parameters.split()[1],
        opm_entity=parameters.split()[2],
        short_description=' '.join(parameters.split()[3:])
    )
    print response


def handle_insert_ci(parameters):
    print "Insert CI option yet not implemented."


insert_options = {
    'incident': handle_insert_incident,
    'ci': handle_insert_ci,
}

get_options = {
    'incident': handle_get_incident,
    'ci': handle_get_ci,
}

options = {
    'insert': insert_options,
    'get': get_options
}
