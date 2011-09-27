# -*- coding: utf-8 -*-

import numpy #@UnusedImport
import numpy.matlib #@Reimport
import os.path
import pylab
import pyplot.data #@UnusedImport
import pyplot.datafile #@Reimport
import sys

class Datafolder(pyplot.data.Data):
    DrawErrorBar = True
    LoadingHook = None
    
    def __init__(self, folderpath = None, basename="data", extension="logtxt", labels=None, datas = None):
        self.stderr = None
        self.__folderpath = folderpath
        self.__basename = basename
        self.__extension = extension
        self.__bins = None
        self._legend = None
        self.sparsePlotFilter = None
        self._counter = None
        if folderpath is not None:
            self._raw = self._loadraw()
        else: 
            self._raw = self._appendraws(datas)
        super(Datafolder, self).__init__(labels=labels)
        
    @property
    def folderpath(self):
        return self.__folderpath

    def __getdatafilename(self, counter):
        filepath = "%s/%s%02d.%s" % (self.__folderpath, self.__basename, counter, self.__extension)
        if not os.path.isfile(filepath):
            filepath += ".gz"
        if not os.path.isfile(filepath) or not os.path.getsize(filepath) > 0:
            return None
        return filepath

    def __getfiles(self):
        assert os.path.isdir(self.__folderpath), self.__folderpath
        self._counter = 0
        nextfile = self.__getdatafilename(self._counter)
        files = []
        while nextfile is not None:
            files.append(nextfile)
            self._counter += 1
            nextfile = self.__getdatafilename(self._counter)
        return files
    
    def binData(self, bins):
        self.__bins = bins
        blockSize = self._raw.shape[0] / self.__bins
        binraw = numpy.matlib.zeros((self.__bins, self._raw.shape[1]))
        sampledstderr = numpy.matlib.zeros((self.__bins, self._raw.shape[1]))
        for b in xrange(self.__bins):
            blockBegin = blockSize * b
            binraw[b,:] = numpy.mean(self._raw[blockBegin:blockBegin + blockSize,:], axis=0)
            sampledstderr[b,:] = self.stderr[blockBegin + blockSize / 2,:]
        self._raw = binraw
        self.stderr = sampledstderr 
    
    @property
    def nbFiles(self):
        return self._counter
    
    def __extractBlock(self, x, blockSize, i):
        block = numpy.matlib.zeros((self.__bins, x.shape[1]))
        for b in xrange(self.__bins):
            block[b] = x[b * blockSize + i]
        return block

    def __appendraw(self, n, mean, m2, x):
        if n is None:
            n = 0
            shape = x.shape if self.__bins is None else (self.__bins, x.shape[1])
            mean = numpy.matlib.zeros(shape)
            m2 = numpy.matlib.zeros(shape)
        n += 1
        delta = x - mean
        mean = mean + delta / n
        m2 = m2 + numpy.multiply(delta, x - mean) #@UndefinedVariable
        return n, mean, m2

    def _loadraw(self):
        files = self.__getfiles()
        if not files: 
            print >> sys.stderr, "Nothing to load in %s" % os.path.abspath(self.__folderpath)
            return None
        (n, mean, m2) = (None, None, None)
        shape = None
        for filepath in files:
            datafile = pyplot.datafile.Datafile(filepath)
            if shape is None:
                shape = datafile.raw.shape
            elif shape != datafile.raw.shape:
                print "%s is different from the previous shape %s. Aborting." % (datafile.raw.shape, shape)
                break
            if self._legend is None:
                self._legend = datafile.legend
            (n, mean, m2) = self.__appendraw(n, mean, m2, datafile.raw)
            if self.LoadingHook:
                self.LoadingHook(self)
        variance = m2 / (n - 1) if n > 1 else None
        # Standard error of the mean
        self.stderr = (numpy.sqrt(variance/(n - 1)) / numpy.sqrt(n - 1) if n > 1
                       else numpy.zeros(mean.shape))
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
        indexes = list(i * space + offset for i in range(0, nbErrorBar) 
                       if self.sparsePlotFilter is None or self.sparsePlotFilter(i))
        sxdata = list(xdata[i] for i in indexes)
        sydata = list(ydata[i] for i in indexes)
        syerr = list(yerr[i] for i in indexes)
        return sxdata, sydata, syerr

    def _plot(self, xdata, yaxis,  **kwargs):
        sparseErrorBar = 0
        if kwargs.has_key('sparseErrorBar') and kwargs['sparseErrorBar'] > 0:
            sparseErrorBar = kwargs['sparseErrorBar']
            del kwargs['sparseErrorBar']
        elinewidth = 1
        if kwargs.has_key('elinewidth'):
            elinewidth = kwargs['elinewidth']
            del kwargs['elinewidth']
        capsize = 3
        if kwargs.has_key('capsize'):
            capsize = kwargs['capsize']
            del kwargs['capsize']
        super(Datafolder, self)._plot(xdata, yaxis, **kwargs)
        ydata = list(self.raw[:,yaxis].flat)
        yerr = list(self.stderr[:,yaxis].flat)
        if not self.DrawErrorBar:
            return
        if sparseErrorBar > 0:
            xdata, ydata, yerr = self.sparsify(yaxis, xdata, ydata, yerr, sparseErrorBar)
        pylab.errorbar(xdata, ydata, yerr = yerr, color = self._color(yaxis), 
                       marker='None', linestyle='None', elinewidth = elinewidth, capsize = capsize)

    def iterrows_stderr(self):
        return (list(self.stderr[i,:].flat) for i in xrange(0, self.stderr.shape[0]))


def load(path, basename="data", extension='logtxt', **kwargs):
    default_file_path = path + '/' + basename + '.' + extension
    if os.path.isfile(default_file_path):
        return pyplot.datafile.Datafile(default_file_path, **kwargs)
    if os.path.isdir(path):
        return Datafolder(path, basename, **kwargs)
    return pyplot.datafile.Datafile(path, **kwargs)
