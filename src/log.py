# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import yaml
import logging
import logging.config

try:
    import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    print e
    sys.exit(-1)

import servicenow_conf


if not os.path.exists(servicenow_conf.LOG_PATH):
    os.mkdir(servicenow_conf.LOG_PATH)

logging_conf_file = open(__meta__.PATHS['CONF_PATH'] + '/logging.yaml', 'r')
logging_conf_dict = yaml.load(logging_conf_file.read())
logging_conf_file.close()

for handler in logging_conf_dict['handlers']:
    for attribute in logging_conf_dict['handlers'][handler]:
        if attribute == 'filename':
            logging_conf_dict['handlers'][handler][attribute] = (
                __meta__.LOG_PATH + '/' +
                logging_conf_dict['handlers'][handler][attribute]
            )

logging.config.dictConfig(logging_conf_dict)
userMessage = logging.getLogger()
alertEventsNotInserted = logging.getLogger('alertEventsNotInserted')
alertEventsNotInsertedTemp = logging.getLogger('alertEventsNotInsertedTemp')
pastAlertEvents = logging.getLogger('pastAlertEvents')
pastAlertEventsTemp = logging.getLogger('pastAlertEventsTemp')
