#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from distutils.core import *
from distutils.file_util import *
from py2exe import *

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  

setup(
    zipfile=None,
    options = {
        "py2exe": {
            'unbuffered': True,
            'optimize': 2,
            'bundle_files': 1,
            'excludes': ['_ssl',  # Exclude _ssl
                   'pyreadline', 'difflib', 'doctest', 'locale',
                  'optparse', 'calendar'],  # Exclude standard library
            'dll_excludes': ['w9xpopen.exe'],  # Exclude msvcr71
            'compressed': True,  # Compress library.zip
        }
    }
)
copy_file('conf/servicenow_conf.py', 'dist')
