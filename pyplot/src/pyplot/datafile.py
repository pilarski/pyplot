# -*- coding: utf-8 -*-

import numpy
import os
import pyplot.data

class Datafile(pyplot.data.Data):
    def __init__(self, filepath, labels=None):
        self.__filepath = filepath
        self._legend = self._readlegend()
        self._raw = self._loadraw()
        super(Datafile, self).__init__(labels=labels)
        self.__date = os.stat(self.__filepath).st_mtime

    def _loadraw(self):
        print("Loading %s..." % self.__filepath)
        skipped = 0 if self.legend is None else 1
        return numpy.loadtxt(self.__filepath, skiprows=skipped) #@UndefinedVariable

    def _readlegend(self):
        f = open(self.__filepath, 'r')
        line = iter(f).next()
        f.close()
        if line[0].isdigit() or line[0] == '.':
            return None
        return line.split()
