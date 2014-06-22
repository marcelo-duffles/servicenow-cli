# !/usr/bin/env python
# -*- coding:utf-8 -*-

import yaml
import logging
import logging.config


logging_conf_file = open('conf/logging.yaml', 'r')
logging_conf_dict = yaml.load(logging_conf_file.read())
logging_conf_file.close()
logging.config.dictConfig(logging_conf_dict)
userMessage = logging.getLogger()
alertEventsNotInserted = logging.getLogger('alertEventsNotInserted')
alertEventsNotInsertedTemp = logging.getLogger('alertEventsNotInsertedTemp')
pastAlertEvents = logging.getLogger('pastAlertEvents')
pastAlertEventsTemp = logging.getLogger('pastAlertEventsTemp')
