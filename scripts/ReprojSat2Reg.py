#! /scripts/goes/anaconda/env-radiacao/bin/python
# coding: utf-8

__author__ = "Marcio Britto"

import numpy as np

##------Function to cut area ---------##
def CutArea(lat, lon, beginLatReg, endLatReg, beginLonReg, endLonReg):
	
    rows, cols = np.where((lat>=beginLatReg) & (lat<=endLatReg) & (lon>=beginLonReg) & (lon<=endLonReg))

    return rows, cols


##------Function to reproject image from satelite to regular ---------##
def Reproj2Reg(lat, lon, data, beginLatReg, endLatReg, beginLonReg, endLonReg, degree):

   
   y = np.arange(endLatReg-0.04, beginLatReg-0.04, -(degree))
   x = np.arange(beginLonReg, endLonReg, degree)
   xx, yy = np.meshgrid(x, y)

   dataGrided = np.zeros((xx.shape[0], xx.shape[1]), float)

   Yindex = np.array((((yy.max()-0.01) - lat)/degree), int)
   Xindex = np.array(((lon - (xx.min()+0.01))/degree), int)

   dataGrided[Yindex,Xindex]= data

   return dataGrided, xx, yy
