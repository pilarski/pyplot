# -*- coding: utf-8 -*-

import pylab
import numpy

class Data(object):
    def __init__(self, labels = None):
        self.__labels = {} if labels is None else dict(labels)
        self.__setattr()
        self.__line = {}
        
    def reload(self):
        self._raw = self._loadraw()
        self._legend = self._readlegend()
        
    def toFieldLabel(self, label):
        result = label
        result = result.replace('[','')
        result = result.replace(']','')
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
        xdata = self.raw[:,xaxis].flat if xaxis else None
        for yaxis in yaxes:
            self._plot(xdata, yaxis, **kwargs)
        # pylab.legend(loc=0)

    @property
    def raw(self):
        return self._raw

    @property
    def legend(self):
        return None if self._legend is None else list(self._legend)

