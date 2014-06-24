# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_PATH = BASE_PATH + '/log'
    PATHS = {
        'BASE_PATH': BASE_PATH,
        'SRC_PATH': os.path.join(BASE_PATH, "src"),
        'CONF_PATH': os.path.join(BASE_PATH, "conf")}
except Exception, e:
    print e


if __name__ == "__main__":
    print PATHS
