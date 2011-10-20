# -*- coding: utf-8 -*-

import gzip
import numpy
import os
import pyplot.data
import sys

class Datafile(pyplot.data.Data):
    def __init__(self, filepath, labels=None):
        self._filepath = filepath
        if self.Verbose:
            print("Loading %s..." % self._filepath)
        try:
            self._legend = self._readlegend()
            self._raw = self._loadraw()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self._legend = []
            self._raw = numpy.zeros((0,0))
        super(Datafile, self).__init__(labels=labels)
        self.__date = os.stat(self._filepath).st_mtime

    def _loadraw(self):
        skipped = 0 if not self.legend else 1
        return numpy.loadtxt(self._filepath, skiprows=skipped) #@UndefinedVariable

    def _readlegend(self):
        openfile = gzip.open if self._filepath.endswith('.gz') else open
        f = openfile(self._filepath, 'r') 
        line = iter(f).next()
        f.close()
        if line[0].isdigit() or line[0] == '.':
            return None
        return line.split()


    def binDataSingle(self, bins):
	""" PMP Edit """
        self.__bins = bins
        blockSize = self._raw.shape[0] / self.__bins
        binraw = numpy.matlib.zeros((self.__bins, self._raw.shape[1]))
        for b in xrange(self.__bins):
            blockBegin = blockSize * b
            binraw[b,:] = numpy.mean(self._raw[blockBegin:blockBegin + blockSize,:], axis=0)
        self._raw = binraw