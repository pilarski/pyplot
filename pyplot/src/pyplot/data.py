# -*- coding: utf-8 -*-

import pylab
import numpy

# pylint: disable-msg=W0201
class Data(object):
    Verbose = True
    
    def __init__(self, labels = None):
        self.__labels = {} if labels is None else dict(labels)
        self.__setattr()
        self.__line = {}
        
    def reload(self):
        self._raw = self._loadraw()
        self._legend = self._readlegend()
        
    def _loadraw(self):
        raise NotImplemented()
        
    def _readlegend(self):
        raise NotImplemented()
        
    def toFieldLabel(self, label):
        result = label
        result = result.replace('[','')
        result = result.replace(']','')
        result = result.replace('/','')
        result = result.replace(':','')
        result = result.replace('.','')
        if result[0].isdigit():
            result = "_" + result 
        return result

    def __setattr(self):
        if self._legend is None:
            return
        for (index, label) in enumerate(self._legend):
            setattr(self, self.toFieldLabel(label), index)

    def _plot(self, xdata, yaxis, **kwargs):
        ydata = self.raw[:, yaxis].flat
        if not kwargs.has_key('label'):
            kwargs['label'] = self.__labels.get(self._legend[yaxis], self._legend[yaxis])
        self.__line[yaxis] = (pylab.plot(xdata, ydata, **kwargs)[0] if xdata
                              else pylab.plot(ydata, **kwargs)[0])

    def _color(self, yaxis):
        return self.__line[yaxis].get_color()

    def __tolist(self, yaxes):
        if type(yaxes) is list:
            return yaxes
        return [yaxes]

    def plot(self, xaxis, yaxes, **kwargs):
        yaxes = self.__tolist(yaxes)
        xdata = list(self.raw[:,xaxis].flat) if xaxis is not None else range(self.raw.shape[0])
        for yaxis in yaxes:
            self._plot(xdata, yaxis, **kwargs)
        # pylab.legend(loc=0)

    def iterrows(self):
        return (list(self._raw[i,:].flat) for i in xrange(0, self._raw.shape[0]))

    @property
    def raw(self):
        return self._raw

    @property
    def legend(self):
        return None if self._legend is None else self._legend

    def indexOf(self, label):
        return self.legend.index(label)


    def binDataSingle(self, bins):
	""" PMP Edit """
        self.__bins = bins
        blockSize = self._raw.shape[0] / self.__bins
        binraw = numpy.matlib.zeros((self.__bins, self._raw.shape[1]))
        for b in xrange(self.__bins):
            blockBegin = blockSize * b
            binraw[b,:] = numpy.mean(self._raw[blockBegin:blockBegin + blockSize,:], axis=0)
        self._raw = binraw

