#! /scripts/goes/anaconda/env-radiacao/bin/python
# coding: utf-8

__author__ = "Marcio Britto"

##----------REGULAR FUNCTIONS---------##

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

os.environ['PROJ_LIB'] = "/scripts/goes/anaconda/env-radiacao/share/proj"
from mpl_toolkits.basemap import Basemap
plt.switch_backend('agg')

#-----------Function Calculates Julian Day
def calcDayJul(yearI, monthI, dayI):
    
    yearJul = [0,31,59,90,120,151,181,212,243,273,304,334,365]

    if ((yearI % 4) == 0 ) and (monthI > 2):
        dayJ=yearJul[monthI-1]+ dayI +1
    else:
        dayJ=yearJul[monthI-1]+ dayI

    
    return dayJ

##---------Funtion to plot image - regular grid-------##
def doDataPlot(lonMatrix, latMatrix, data, beginLatReg, endLatReg, 
               beginLonReg, endLonReg, outputIMG, titleIMG):

    beginLatFig = beginLatReg
    endLatFig = endLatReg
    beginLonFig = beginLonReg
    endLonFig = endLonReg

    plt.figure(figsize=(15,15))

    m=Basemap(projection='cyl',resolution='l',llcrnrlat=beginLatFig,
      urcrnrlat=endLatFig,llcrnrlon=beginLonFig,urcrnrlon=endLonFig)

  
    #data = np.ma.masked_where(data < 0.01, data)

    cmap = mpl.colors.ListedColormap([
       [ 0.   ,  0.   ,  0.545],
       [ 0.   ,  0.   ,  1.   ],
       [ 0.118,  0.565,  1.   ],
       [ 0.529,  0.808,  0.98 ],
       [ 0.4  ,  0.804,  0.667],
       [ 0.604,  0.804,  0.196],
       [ 1.   ,  1.   ,  0.   ],
       [ 1.   ,  0.647,  0.   ],
       [ 1.   ,  0.498,  0.314],
       [ 1.   ,  0.   ,  0.   ]])

    cmap.set_under((1, 1, 1))
    cmap.set_over((0, 0, 0))
    m.pcolormesh(lonMatrix, latMatrix, data, cmap=cmap, vmin=1., vmax=500.)

    #parallels = np.arange(beginLatFig,endLatFig,5.)
    #m.drawparallels(parallels,labels=[1,0,0,1],fontsize="15")
    #meridians = np.arange(beginLonFig,endLonFig,10.)
    #m.drawmeridians(meridians,labels=[1,0,0,1], fontsize="15")
    
    
    #m.drawcountries(linewidth=1.5)
    #m.drawcoastlines(linewidth=1.5)
    #m.drawstates(linewidth=1.5)
    
    #cb = m.colorbar(ticks=[50,100,150,200,250,300,350,400,450])
    #cb.ax.tick_params(labelsize=16)
    #plt.colorbar()
    
    plt.savefig(outputIMG,format='png',bbox_inches="tight", pad_inches=-0.1, dpi=158, frameon=False)
    #plt.title(titleIMG, fontsize="30")
    #plt.savefig(outputIMG,format='png',bbox_inches='tight', dpi=100)
    #plt.show()
    
    
def createBin(Matrix, pathBin):
    
    outputBin = open(pathBin,"wb")
    output = Matrix*10.
    output = np.around(output, decimals=0)
    output = output.astype(np.uint16)

    outputBin.write(output)
    outputBin.close()

    return output
    


# In[ ]:

# metodo para preencher as lacunas nos dados 
def getCompleted(data,dataAux):
    
    numberCol = data.shape[1]
    
    data = np.vstack((data,np.zeros(numberCol)))
    data = np.vstack((np.zeros(numberCol),data))
    
    numberRol = data.shape[0]

    zerosMatrix = np.zeros(numberRol)
    zerosMatrix = zerosMatrix.reshape(numberRol,1) 

    data = np.hstack((data,zerosMatrix))

    dataOriginal = np.hstack((zerosMatrix,data))


    a1=np.array([-1]+range(dataOriginal.shape[1])[0:-1])
    a1 = dataOriginal[:,a1]

    a2 = np.array(range(dataOriginal.shape[1])[1:]+[0])
    a2 = dataOriginal[:,a2]

    a3=np.array(range(dataOriginal.shape[0])[1:]+[0])
    a3 = dataOriginal[a3]

    a4 = np.array([-1]+range(dataOriginal.shape[0])[0:-1])
    a4 = dataOriginal[a4]

    a5 = np.array(range(dataOriginal.shape[0])[1:]+[0])
    a5 = a2[a5]

    a6 = np.array(range(dataOriginal.shape[0])[1:]+[0])
    a6 = a1[a6]

    a7 = np.array(range(dataOriginal.shape[1])[1:]+[0])
    a7 = a4[:,a7]

    a8 = np.array([-1]+range(dataOriginal.shape[1])[0:-1])
    a8 = a4[:,a8]

    aSumation = a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8

    dataAverage = aSumation/8

    dataOriginal[dataAux == 0.] = dataAverage[dataAux == 0.]
    dataOriginal = dataOriginal[1:-1,1:-1]
    
    return dataOriginal
