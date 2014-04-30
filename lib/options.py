#!/usr/bin/env python 
#-*- coding:utf-8 -*- 

import traceback 
import sys

try:
    from lib import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    print e
    sys.exit(-1)

import soap_api
import servicenow_conf

def handle_get_incident_option():
    print 'Get incident option yet not implemented.'

def handle_insert_incident_option(parameters):
    session = soap_api.login()
    soap_api.insert_incident(parameters, session)    

insert_options = {
    'incident': handle_insert_incident_option,                  
}

get_options = {
    'incident': handle_get_incident_option,                  
}


options = {
    'insert': insert_options,
    'get': get_options
}

