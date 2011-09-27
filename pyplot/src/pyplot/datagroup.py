# -*- coding: utf-8 -*-

import data
import os
import os.path
import pylab
import pyplot.datafolder

class DataGroup(object):
    DrawErrorBar = True
    
    def __init__(self, folderpath, groupPrefix = "", **kwargs):
        self.folderpath = folderpath
        prefixes = self.searchprefixes(groupPrefix)
        self.__legend = None
        self.__kwargs = kwargs
        self.datas = self.loaddatasfromprefixes(prefixes)
        self.__setattr()
        self.labels = {}
        
    def setLabels(self, labels):
        self.labels = labels
                
    def __setattr(self):
        for (index, label) in enumerate(self.__legend):
            setattr(self, label, index)

    # pylint: disable-msg=W0621
    def loaddatasfromprefixes(self, prefixes):
        datas = {}
        for (prefix, isdir) in prefixes:
            data = (pyplot.datafolder.load(self.folderpath + '/' + prefix, **self.__kwargs) if isdir 
                    else pyplot.datafolder.load(self.folderpath, prefix, **self.__kwargs))
            if data.raw is None:
                continue
            #if isdir:
            #    data.sparsePlotFilter = (lambda j: j % len(prefixes) == i)
            if self.__legend is None:
                self.__legend = data.legend
            datas[prefix] = data
            setattr(self, prefix, data)
        return datas
        
    def __filefilter(self, groupPrefix, path):
        if os.path.split(path)[1].startswith('.'):
            return False
        if groupPrefix and not os.path.split(path)[1].startswith(groupPrefix):
            return False
        if not path.endswith('logtxt') and not os.path.isdir(path):
            return False
        return True
    
    def binData(self, bins):
        for label, dataFolder in self.datas.iteritems():
            if data.Data.Verbose:
                print "Binning " + label + "..."
            dataFolder.binData(bins)
    
    def extractprefix(self, filename):
        if os.path.isdir(filename):
            return os.path.split(filename)[1]
        basename = (os.path.split(filename)[1])[0:filename.index('.')]
        endprefixindex = len(basename) - 1
        while basename[endprefixindex].isdigit():
            endprefixindex -= 1
        return basename[0:endprefixindex + 1]
        
    def searchprefixes(self, groupPrefix):
        assert os.path.isdir(self.folderpath), self.folderpath
        prefixes = set()
        for filename in os.listdir(self.folderpath):
            filepath = self.folderpath + '/' + filename
            if not self.__filefilter(groupPrefix, filepath):
                continue
            prefixes.add((self.extractprefix(filepath), 
                          os.path.isdir(filepath)))
        return prefixes
    
    def plot(self, xdata, yaxis,  **kwargs):
        for key, value in self.datas.iteritems():
            value.DrawErrorBar = self.DrawErrorBar
            label = self.labels.get(key, key)
            value.plot(xdata, yaxis, label=label, **kwargs)
            
    @property
    def legend(self):
        return self.__legend
            
if __name__ == '__main__':
    d = DataGroup('/Users/thomas/Codes/Research/Critterbot/rlpark.plugin.playground/results/randomexplo')
    print d.legend
    d.plot(d.N, d.NbSteps)
    pylab.show()

