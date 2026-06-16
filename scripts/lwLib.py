#! /scripts/goes/anaconda/env-radiacao/bin/python
# coding: utf-8


import numpy as np


__author__ = "Marcio Britto"


##---------LONG WAVE FUNCTIONS---------##


##--------planck law-------##
def planck(tem, lam):
    
    k = 1.38
    c =3
    h = 6.62
    
    rad = (2*h*c**2)*10**(12)/((lam**5)*(np.exp(h*c*10**(5)/(k*tem*lam))-1))
    return rad


##--------long wave calculation------------#
def longWaveModel(data):

    a0 = -493.7
    a11 = -16.96
    alpha = 0.187

    b = 47
    c = 0.76

    Temp11 = data    
    E11_11 = planck(data, 11)
    longwave = a0 + a11 * E11_11 + alpha*(b + c*Temp11)**(1.52)
    
    return longwave


