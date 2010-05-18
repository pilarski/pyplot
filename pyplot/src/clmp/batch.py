# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import clmp.dt3d
import os
import os.path
import pylab

SubFolder = 'pictures'

def convert(folder, filename):
    d = clmp.dt3d.DT3D(folder + '/' + filename)
    d.plot()
    pylab.savefig(folder + '/' + SubFolder + '/' + filename + '.png', format='png', dpi=100)

def main(folder):
    if not os.path.isdir(folder + '/' + SubFolder):
        os.mkdir(folder + '/' + SubFolder)
    for filename in os.listdir(folder):
        if not filename.endswith(clmp.dt3d.DT3D.Extension):
            continue
        print filename
        convert(folder, filename)

if __name__ == '__main__':
    main('/Users/thomas/Codes/Research/Critterbot/playground/results/mountaincaroffpolicy')