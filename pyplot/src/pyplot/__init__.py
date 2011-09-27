# -*- coding: utf-8 -*-

import os.path
import pyplot.datafolder
import pyplot.datagroup
import cPickle

def load(path, basename="data", **kwargs):
    return pyplot.datafolder.load(path, basename, **kwargs)

def loadgroup(path, **kwargs):
    return pyplot.datagroup.DataGroup(path, **kwargs)

def loadgroupcached(path, forceLoading = False, **kwargs):
    cachePath = path + '/pyplot.cache'
    if (os.path.exists(cachePath) and not forceLoading):
        print "Loading from " + cachePath
        f = open(cachePath, 'rb')
        data = cPickle.load(f)
        f.close()
        return data
    data = loadgroup(path, **kwargs)
    f = open(cachePath, 'wb')
    cPickle.dump(data, f)
    print "Saved in " + cachePath
    f.close()
    return data
    
    
def prepareFolder(folderPath):
    if os.path.isdir(folderPath):
        return
    os.makedirs(folderPath)