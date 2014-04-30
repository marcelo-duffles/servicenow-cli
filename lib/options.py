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
    data = {'impact': '1',
	    'urgency': '1',
	    'priority': '1',
	    'category': 'High',
	    'location': 'San Diego',
	    'user': 'fred.luddy@yourcompany.com',
	    'assignment_group': 'Technical Support', 
            'assigned_to': 'David Loo',
	    'short_description': parameters,
            'comments': 'This a test making an incident with python.\nIsn\'t life wonderful?'}
    soap_api.insert_incident(data, session)    

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

