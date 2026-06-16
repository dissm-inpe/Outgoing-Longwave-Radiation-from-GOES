#! /scripts/goes/anaconda/env-radiacao/bin/python
# -*- coding: utf-8 -*-

__author__ = "Renato galante"
__email__ = "renato.galante@inpe.br"

import argparse
import numpy as np
from netCDF4 import Dataset
import re
import scipy as sp
import scipy.ndimage


def goes19_loadimg(nc_infile):
    fh = Dataset(nc_infile, mode='r')

    ydim = fh.dimensions['y'].size
    xdim = fh.dimensions['x'].size
    wl_central = fh.variables['band_wavelength'][0]
    
    print 'IMG Size = {}x{}'.format(xdim, ydim)
    
    tempo_inc = fh.time_coverage_start #fh.variables['time_bounds'][:]
    tempo_fim = fh.time_coverage_end
    
    tempo_inc = re.split('-|T|:', tempo_inc)
    tempo_fim = re.split('-|T|:', tempo_fim)
    
    satellite_id = fh.platform_ID

    a1 = 0
    a2 = xdim
    b1 = 0
    b2 = ydim

    cmi = fh.variables['CMI'][a1:a2, b1:b2]
    
    return dict(tb=cmi, nx=xdim, ny=ydim, ti=tempo_inc, tf=tempo_fim, wl=wl_central, satid=satellite_id)
    
#Autor: Marcio Britto
##------Rescale for temperature: cubic interpolation
def degrade(infile, degree):

    resample = int(100 * degree)

    x = goes19_loadimg(infile)

    x2 = np.full((x['nx'], x['ny']), -1, dtype=np.int16)
    x2 = x['tb']

    print 'resample-factor', resample

    x2 = sp.ndimage.zoom(x2, 0.5, order=3)

    print 'x2 size =', x2.shape


    return x2

   
