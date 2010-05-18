# -*- coding: utf-8 -*-

import matplotlib
import numpy
import pylab

class DT3D(object):
    Extension = 'dt3d'
    
    def __init__(self, filename):
        self.filename = filename
        self.raw = numpy.loadtxt(filename)
        assert self.raw.shape[0] == self.raw.shape[1]
        self.xrange = (0, 1)
        self.yrange = (0, 1) 
        
    def plot(self):
        pylab.clf()
        x = numpy.linspace(self.xrange[0], self.xrange[1], self.dim)
        y = numpy.linspace(self.yrange[0], self.yrange[1], self.dim)
        ax = pylab.gca()
        im = matplotlib.image.NonUniformImage(ax, #interpolation='bilinear', 
                                              extent=(self.xrange[0], self.xrange[1],
                                                      self.yrange[0], self.yrange[1]))
        im.set_data(x, y, self.raw)
        ax.images.append(im)
        ax.set_xlim(self.xrange[0], self.xrange[1])
        ax.set_ylim(self.yrange[0], self.yrange[1])
        pylab.colorbar(im)

    @property
    def dim(self):
        return self.raw.shape[0]
