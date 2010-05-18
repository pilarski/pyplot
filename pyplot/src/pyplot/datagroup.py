# -*- coding: utf-8 -*-

import os
import os.path
import pylab
import pyplot.datafolder

class DataGroup(object):
    DrawErrorBar = True
    
    def __init__(self, folderpath):
        self.folderpath = folderpath
        prefixes = self.searchprefixes()
        self.__legend = None
        self.datas = self.loaddatasfromprefixes(prefixes)
        self.__setattr()
                
    def __setattr(self):
        for (index, label) in enumerate(self.__legend):
            setattr(self, label, index)

    def loaddatasfromprefixes(self, prefixes):
        datas = {}
        for prefix in prefixes:
            data = pyplot.datafolder.load(self.folderpath, prefix)
            if self.__legend is None:
                self.__legend = data.legend
            datas[prefix] = data
            setattr(self, prefix, data)
        return datas
        
    def __filefilter(self, filename):
        if filename.startswith('.'):
            return False
        if not filename.endswith('logtxt'):
            return False
        return True
    
    def extractprefix(self, filename):
        basename = filename[0:filename.index('.')]
        endprefixindex = len(basename) - 1
        while basename[endprefixindex].isdigit():
            endprefixindex -= 1
        return basename[0:endprefixindex + 1]
        
    def searchprefixes(self):
        assert os.path.isdir(self.folderpath), self.folderpath
        prefixes = set()
        for filename in os.listdir(self.folderpath):
            if not self.__filefilter(filename):
                continue
            prefixes.add(self.extractprefix(filename))
        return prefixes
    
    def plot(self, xdata, yaxis,  **kwargs):
        for key, value in self.datas.iteritems():
            value.DrawErrorBar = self.DrawErrorBar
            value.plot(xdata, yaxis, label=key, **kwargs)
            
    @property
    def legend(self):
        return self.__legend
            
if __name__ == '__main__':
    d = DataGroup('/Users/thomas/Codes/Research/Critterbot/rlpark.plugin.playground/results/randomexplo')
    print d.legend
    d.plot(d.N, d.NbSteps)
    pylab.show()

