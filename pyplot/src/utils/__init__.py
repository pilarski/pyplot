# -*- coding: utf-8 -*-

import os.path
import sys

def load(filepath):
    abs_filepath = os.path.abspath(filepath)
    folder, filename = os.path.split(abs_filepath)
    sys.path.append(folder)
    module_name = filename[:filename.rindex('.')]
    return __import__(module_name)
