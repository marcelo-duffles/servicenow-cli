# !/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
from SOAPpy import SOAPProxy
from src import log

try:
    import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    log.userMessage.error(e)
    sys.exit(-1)

import servicenow_conf


def build_session(resource):
    """returns a SOAP session."""

    proxy = 'https://%s:%s@%s.service-now.com/%s.do?SOAP' %\
            (servicenow_conf.USERNAME, servicenow_conf.PASSWORD,
             servicenow_conf.INSTANCE, resource)
    namespace = 'http://www.service-now.com/'

    try:
        session = SOAPProxy(proxy, namespace)

        if (servicenow_conf.SOAP_API_DEBUG):
            session.config.dumpHeadersIn = 1
            session.config.dumpHeadersOut = 1
            session.config.dumpSOAPOut = 1
            session.config.dumpSOAPIn = 1

        return session
    except Exception, e:
        log.userMessage.error(e)
        sys.exit(-1)


def insert(resource, data):
    session = build_session(resource)
    """ See https://yourinstance.service-now.com/desiredresource.do?WSDL """
    """ for available values """
    response = session.insert(**data)
    return response


def get(resource, data):
    session = build_session(resource)

    resource_keys = session.getKeys(**data)
    if (resource_keys.sys_id == ''):
        raise Exception('Object not found in Service Now: %s' % data)

    response = session.get(
        sys_id=resource_keys.sys_id
    )
    return response
