#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATHS = {
        'BASE_PATH' : BASE_PATH,
        'LIB_PATH' : os.path.join(BASE_PATH, "lib"),
        'CONF_PATH' : os.path.join(BASE_PATH, "conf"),}
except Exception, e:
    print e


if __name__ == "__main__":
    print PATHS
