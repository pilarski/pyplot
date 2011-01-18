# -*- coding: utf-8 -*-

import numpy #@UnusedImport
import numpy.matlib #@Reimport
import os.path
import pylab
import pyplot.data #@UnusedImport
import pyplot.datafile #@Reimport

class Datafolder(pyplot.data.Data):
    DrawErrorBar = True
    
    def __init__(self, folderpath = None, basename="data", extension="logtxt", labels=None, datas = None):
        self.stderr = None
        self.__folderpath = folderpath
        self.__basename = basename
        self.__extension = extension
        self._legend = None
        if folderpath is not None:
            self._raw = self._loadraw()
        else: 
            self._raw = self._appendraws(datas)
        super(Datafolder, self).__init__(labels=labels)

    def __getdatafilename(self, counter):
        filepath = "%s/%s%02d.%s" % (self.__folderpath, self.__basename, counter, self.__extension)
        if not os.path.isfile(filepath):
            filepath += ".gz"
        if not os.path.isfile(filepath) or not os.path.getsize(filepath) > 0:
            return None
        return filepath

    def __getfiles(self):
        assert os.path.isdir(self.__folderpath), self.__folderpath
        counter = 0
        nextfile = self.__getdatafilename(counter)
        files = []
        while nextfile is not None:
            files.append(nextfile)
            counter += 1
            nextfile = self.__getdatafilename(counter)
        return files

    def __appendraw(self, n, mean, m2, x):
        if n is None:
            n = 0
            mean = numpy.matlib.zeros(x.shape)
            m2 = numpy.matlib.zeros(x.shape)
        n += 1
        delta = x - mean
        mean = mean + delta / n
        m2 = m2 + numpy.multiply(delta, x - mean) #@UndefinedVariable
        return n, mean, m2

    def _loadraw(self):
        files = self.__getfiles()
        assert files, "Nothing to load in %s" % os.path.abspath(self.__folderpath)
        (n, mean, m2) = (None, None, None)
        shape = None
        for filepath in files:
            datafile = pyplot.datafile.Datafile(filepath)
            if shape is None:
                shape = datafile.raw.shape
            elif shape != datafile.raw.shape:
                continue
            if self._legend is None:
                self._legend = datafile.legend
            (n, mean, m2) = self.__appendraw(n, mean, m2, datafile.raw)
        variance = m2 / (n - 1)
        self.stderr = numpy.sqrt(variance/n)
        return mean
    
    def _appendraws(self, datas):
        (n, mean, m2) = (None, None, None)
        for datafile in datas:
            if self._legend is None:
                self._legend = datafile.legend
            (n, mean, m2) = self.__appendraw(n, mean, m2, datafile.raw)
        variance = m2 / (n - 1)
        self.stderr = numpy.sqrt(variance/n)
        return mean

    def sparsify(self, yaxis, xdata, ydata, yerr, nbErrorBar):
        space = len(xdata) / nbErrorBar
        offset = int(yaxis / self.raw.shape[1] * space)
        indexes = list(i * space + offset for i in range(0, nbErrorBar))
        sxdata = list(xdata[i] for i in indexes)
        sydata = list(ydata[i] for i in indexes)
        syerr = list(yerr[i] for i in indexes)
        return sxdata, sydata, syerr

    def _plot(self, xdata, yaxis,  **kwargs):
        sparseErrorBar = 0
        if kwargs.has_key('sparseErrorBar') and kwargs['sparseErrorBar'] > 0:
            sparseErrorBar = kwargs['sparseErrorBar']
            del kwargs['sparseErrorBar']
        super(Datafolder, self)._plot(xdata, yaxis, **kwargs)
        ydata = list(self.raw[:,yaxis].flat)
        yerr = list(self.stderr[:,yaxis].flat)
        if not self.DrawErrorBar:
            return
        if sparseErrorBar > 0:
            xdata, ydata, yerr = self.sparsify(yaxis, xdata, ydata, yerr, sparseErrorBar)
        pylab.errorbar(xdata, ydata, yerr = yerr, color = self._color(yaxis), 
                       marker='None', linestyle='None', elinewidth = 1)


def load(path, basename="data", extension='logtxt', **kwargs):
    default_file_path = path + '/' + basename + '.' + extension
    if os.path.isfile(default_file_path):
        return pyplot.datafile.Datafile(default_file_path, **kwargs)
    if os.path.isdir(path):
        return Datafolder(path, basename, **kwargs)
    return pyplot.datafile.Datafile(path, **kwargs)
