#! /scripts/goes/anaconda/env-radiacao/bin/python
# coding: utf-8


##------ MAIN PROGRAM Long Wave MODEL for South America -----------##

# coding: utf-8

__author__ = "Marcio Britto, José Dias"

#modules python-anaconda
import os
import numpy as np
import sys
import time as t

#modules DSA
import ReprojSat2Reg
import lwLib
import RegularFunc
import DegradeFile


##-------------Start TIME
start = t.time()


##---------paths and files---------##
#inputdata='201707021030'
#dirano='2017'
#dirmes='07'

inputdate = sys.argv[1]
diryear = inputdate[0:4]
dirmonth = inputdate[4:6]

print "Executing for date: " +inputdate

outPath = '/'.join(['/dados','goes','goes19_produtos','rad_solar'])
mainPath = '/'.join(['/scripts','goes','goes19','rad_solar','longWaveModel'])
folderBin = '/'.join([outPath, 'rol_3h_bin'])
folderLOG = '/dados/bdi/'

##----Images GOES---------##
pathFile = '/dados/goes/goes19/brutos/ch13/' +diryear+ '/' +dirmonth+ '/S10161313_'+inputdate+'.nc'


ncName = os.path.basename(pathFile)


##-------Files Lat and Lon----------##
latFile = '/'.join([mainPath,'bruto','nav', 'G19_4km_lat.bin'])
lat = np.fromfile(latFile, np.int16)
lat = lat.reshape(2712, 2712)
lat = np.array(lat, float)/100.
lat = np.ma.masked_where(lat < -299, lat)

lonFile = '/'.join([mainPath,'bruto','nav', 'G19_4km_lon_75W.bin'])
lon = np.fromfile(lonFile, np.int16)
lon = lon.reshape(2712, 2712)
lon = np.array(lon, float)/100.
lon = np.ma.masked_where(lon < -299, lon)


##---------Date of File------##
nameDate = ncName[10:22]
year = nameDate[0:4]
month = nameDate[4:6]
day = nameDate[6:8]
hourmin = nameDate[8:12]


##----CREATE YEAR AND MONTH FOLDERS---##
os.system("mkdir -p " +outPath +"/rol_3h_bin/"+str(year))
os.system("mkdir -p " +outPath +"/rol_3h_bin/"+str(year)+"/"+str(month))
os.system("mkdir -p " +outPath +"/rol_3h/"+str(year))
os.system("mkdir -p " +outPath +"/rol_3h/"+str(year)+"/"+str(month))


##---------outputs-----##
titleIMG="Onda Longa Am. Sul GOES 19 - " + nameDate 
outputIMG = outPath +"/rol_3h/"+str(year)+"/"+str(month)+"/S11167049_"+inputdate+".png"
pathBin = outPath +"/rol_3h_bin/"+str(year)+"/"+str(month)+"/S11167039_"+inputdate+".bin"
pathPGW = outPath +"/rol_3h/"+str(year)+"/"+str(month)+"/S11167049_"+inputdate+".pgw"

##--Resolution---##
degree = 0.04


##----Function to degrade 1km to 2km----##
data = DegradeFile.degrade(pathFile, degree) 


##------Geographic area of regular grid-------##
beginLatReg = -50.0
endLatReg = 22.0
beginLonReg = -100.0
endLonReg = -28.0



##-----Cut the area of image---------##
rows, cols = ReprojSat2Reg.CutArea(lat, lon, beginLatReg, endLatReg, beginLonReg, endLonReg)

data = data[rows,cols]
lon = lon[rows, cols]
lat = lat[rows, cols]


##---------Reproject image from satelite to regular------##
dataGrided, lonReg, latReg = ReprojSat2Reg.Reproj2Reg(lat, lon, data, beginLatReg, endLatReg, beginLonReg, endLonReg, degree)


##------Calculate Julian Day-----------##
yearI = int(year)
monthI = int(month)
dayI = int(day)
hourI = int(hourmin[0:2])
minI = int(hourmin[2:])
hourZ = float(hourI) + (float(minI) / 60)

dayJ = RegularFunc.calcDayJul(yearI, monthI, dayI)


# In[3]:

##---------EXECUTION OF THE MODEL ----------## 

longWave = lwLib.longWaveModel(dataGrided)
longWave[longWave < 0.]=0


## --- processo de preenchimento das lacunas --- ##
data = longWave*1
dataAux = longWave*1

numberCol = data.shape[1]
    
dataAux = np.vstack((dataAux,np.zeros(numberCol)))
dataAux = np.vstack((np.zeros(numberCol),dataAux))
    
numberRol = dataAux.shape[0]

zerosMatrix = np.zeros(numberRol)
zerosMatrix = zerosMatrix.reshape(numberRol,1) 

dataAux = np.hstack((dataAux,zerosMatrix))
dataAux = np.hstack((zerosMatrix,dataAux))

#------Function to interpolate 3x3
for i in range(10):
    data = RegularFunc.getCompleted(data, dataAux)
    
## --------------------------------------------- ## 
longWave = data


#---------Functions to plot final results ---------##
RegularFunc.doDataPlot(lonReg, latReg, longWave, beginLatReg, endLatReg,beginLonReg, endLonReg, outputIMG, titleIMG)
print 'Created image .pgn!'

#----------Funciton to create bin file --------##
RegularFunc.createBin(longWave, pathBin)
print 'Created bin file!'


##------Create navigation file-----##
txtPGW = "0.04000000000000 \n0.00000000000000 \n0.00000000000000 \n-0.0400000000000 \n-100.000000000000 \n21.960000000" 
filePGW = open(pathPGW, 'w')
filePGW.writelines(txtPGW)
filePGW.close()


##---------------Create LOG-BDI
tamBIN = os.path.getsize(pathBin)
tamBIN = tamBIN/1024

tamIMG = os.path.getsize(outputIMG)
tamIMG = tamIMG/1024

logBIN = open(folderLOG +"7039_"+inputdate+"_"+str(tamBIN), 'w')
logBIN.close()
logIMG = open(folderLOG +"7049_"+inputdate+"_"+str(tamIMG), 'w')
logIMG.close()



print '- finished! Time:', t.time() - start, 'seconds'


