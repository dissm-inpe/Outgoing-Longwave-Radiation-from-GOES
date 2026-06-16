#! /scripts/goes/anaconda/env-radiacao/bin/python
# coding: utf-8


##------ MAIN PROGRAM LONG WAVE MODELO - DAILY AVERAGE-----------##


__author__ = "Marcio Britto"


#modules python-anaconda
from datetime import datetime, timedelta, date
import sys
import numpy as np
import os
import time as t
import commands

#from remap import buildLatLonGrid
import RegularFunc
import lwLib


##-------------Start TIME
start = t.time()

##-----check if date was passed as argument if not use current date-----##
today = ""

today = sys.argv[1]

if (today == "xx"):
    
    today = datetime.now()
    
    deltaDay = timedelta(1)
    prevDay = today - deltaDay 
   
    day = '%02d' % prevDay.day
    month = '%02d' % prevDay.month
    year = prevDay.year

else:
    year = today[0:4]
    month = today[4:6]
    day = today[6:8]

inputdate = str(year)+str(month)+str(day)
    
print "Executing for date: " +inputdate

##---------paths and files---------##
outPath = '/'.join(['/dados','goes','goes19_produtos','rad_solar'])
mainPath = '/'.join(['/scripts','goes','goes19','rad_solar','longWaveModel'])
folderBin = outPath+'/rol_3h_bin/'+str(year)+"/"+str(month)
folderLOG = '/dados/bdi/'

##----CREATE YEAR AND MONTH FOLDERS---##
os.system("mkdir -p " +outPath +"/rol_media_diaria_bin/"+str(year))
os.system("mkdir -p " +outPath +"/rol_media_diaria_bin/"+str(year)+"/"+str(month))
os.system("mkdir -p " +outPath +"/rol_media_diaria/"+str(year))
os.system("mkdir -p " +outPath +"/rol_media_diaria/"+str(year)+"/"+str(month))


##---------outputs-----##
titleIMG="Onda Longa Diaria Am. Sul GOES 19 - " + inputdate
outputIMG = outPath+"/rol_media_diaria/"+str(year)+"/"+str(month)+"/S11167050_"+inputdate+"0000.png"
pathBin = outPath+"/rol_media_diaria_bin/"+str(year)+"/"+str(month)+"/S11167041_"+inputdate+"0000.bin"
pathPGW = outPath+"/rol_media_diaria/"+str(year)+"/"+str(month)+"/S11167050_"+inputdate+"0000.pgw"


##-----Create list of files for the date------------##
listG19 = commands.getoutput("ls " +folderBin+"/S11167039_"+inputdate+"????.bin")
 

##------verify if output file exists-------##
if (os.path.isfile(pathBin)):
   print "File alredy exist for date: " +inputdate
   sys.exit()    


contentList = listG19.split("\n")
ttfiles = len(contentList)

print "Was found " +str(ttfiles)+ " files! \n"


if (ttfiles < 3):
   print "Total of files is insufficient for date " +inputdate
   sys.exit() 


##------Number Rows x Cols---------##
rows=1800
cols=1800


##----------Create Matrix-----------##
matDaily=np.zeros((rows, cols), float)
matQtd=np.zeros((rows, cols), float)


##-------Loop to open the Files anda Calculate the monthly average----------##
for i in range(0,ttfiles,1):
    
    pathFile = contentList[i]
    
    fileX = os.path.basename(pathFile)
    
    dataX = np.fromfile(pathFile, np.uint16)
    dataX = dataX.reshape(rows,cols)
    dataX = np.array(dataX,float)/10

    matQtd[dataX > 0] = matQtd[dataX > 0]+1
    matDaily = matDaily + dataX

matDaily = matDaily/matQtd

##-------Generate matrix lat and lon-------#

beginLatReg = -50.0
endLatReg = 22.0
beginLonReg = -100.0
endLonReg = -28.0

# Geographic area of regular grid (extent[lower-left-x, lly, upper-right-x, ury])
extent = [beginLonReg, beginLatReg, endLonReg, endLatReg]

# Grid resolution (degrees)
degree = 0.04

#Create lat and lon matrix
#lon, lat = buildLatLonGrid(extent, resolution)
y = np.arange(endLatReg-0.04, beginLatReg-0.04, -(degree))
x = np.arange(beginLonReg, endLonReg, degree)
xx, yy = np.meshgrid(x, y)

#---------Functions to plot final results ---------##
RegularFunc.doDataPlot(xx, yy, matDaily, beginLatReg, endLatReg,beginLonReg, endLonReg, outputIMG, titleIMG)
print 'Created image!'

RegularFunc.createBin(matDaily, pathBin)
print 'Created file!'

##------Create navigation file-----##
txtPGW = "0.04000000000000 \n0.00000000000000 \n0.00000000000000 \n-0.0400000000000 \n-100.000000000000 \n21.96000000000" 
filePGW = open(pathPGW, 'w')
filePGW.writelines(txtPGW)
filePGW.close()


##---------------Create LOG-BDI
tamBIN = os.path.getsize(pathBin)
tamBIN = tamBIN/1024

tamIMG = os.path.getsize(outputIMG)
tamIMG = tamIMG/1024

logBIN = open(folderLOG +"7041_"+inputdate+"0000_"+str(tamBIN), 'w')
logBIN.close()
logIMG = open(folderLOG +"7050_"+inputdate+"0000_"+str(tamIMG), 'w')
logIMG.close()

## Convert binary to netcdf
os.system(mainPath+ "/scripts/conv_bin2nc.sh "+inputdate+"0000"+" 7041") 

print '- finished! Time:', t.time() - start, 'seconds'

