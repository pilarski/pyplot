# -*- coding: utf-8 -*-

import os.path
import pyplot.datafolder
import pyplot.datagroup

def load(path, basename="data", **kwargs):
    return pyplot.datafolder.load(path, basename, **kwargs)

def loadgroup(path, **kwargs):
    return pyplot.datagroup.DataGroup(path, **kwargs)