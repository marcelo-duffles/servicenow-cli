#!/usr/bin/env python 
#-*- coding:UTF-8 -*-

from SOAPpy import SOAPProxy
import sys

try:
    import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    print e
    sys.exit(-1)

import servicenow_conf

def login():
    """returns a SOAP session."""

    proxy = 'https://%s:%s@%s.service-now.com/incident.do?SOAP' % (servicenow_conf.USERNAME, servicenow_conf.PASSWORD, servicenow_conf.INSTANCE)
    namespace = 'http://www.service-now.com/'
    
    try:
        session = SOAPProxy(proxy, namespace)

        # uncomment these for LOTS of debugging output
        #session.config.dumpHeadersIn = 1
        #session.config.dumpHeadersOut = 1
        #session.config.dumpSOAPOut = 1
        #session.config.dumpSOAPIn = 1
        
        return session
    except Exception, e:
        print e


def insert_incident(parameters, session):
    """ See https://yourinstance.service-now.com/incident.do?WSDL for available values """
    response = session.insert(
        cmdb_ci='.'.join(parameters.split()[0].split('.')[0:2]),
        opm_severity=parameters.split()[1],
        opm_entity=parameters.split()[2],
        short_description=' '.join(parameters.split()[3:])
    )
    print response

