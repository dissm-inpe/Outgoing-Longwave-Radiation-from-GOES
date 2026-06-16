#! /scripts/goes/anaconda/env-radiacao/bin/python

# coding: utf-8


##------PROGRAM TO EXECUTE LONG WAVE MODEL WITH GOES 19-----------##


__author__ = "Marcio Britto"

from datetime import datetime, timedelta, date
import commands as cm
import sys
import os
import numpy as np


##-----check if date was passed as argument if not use current date-----##
today = ""

if len(sys.argv) > 1:
    today = sys.argv[1]

if (today == ""):
    
    today = datetime.now()
    currHour = today.hour
    
    if (currHour < 8):

        deltaDay = timedelta(1)
        prevDay = today - deltaDay 
   
        day = '%02d' % prevDay.day
        month = '%02d' % prevDay.month
        year = prevDay.year

    else:

        day = '%02d' % today.day
        month = '%02d' % today.month
        year = today.year

else:
    year = today[0:4]
    month = today[4:6]
    day = today[6:8]

inputdate = str(year)+str(month)+str(day)
    
print "Executing for date: " +inputdate


#------PATHS------------------##
outPath = '/'.join(['/dados','goes','goes19_produtos','rad_solar'])
mainPath = '/'.join(['/scripts','goes','goes19','rad_solar','longWaveModel'])
folderBin = '/'.join([outPath, 'rol_3h_bin'])
dataPath = "/dados/goes/goes19/brutos/ch13/"+str(year)+"/"+str(month)+"/"

##------List Files GOES-19------##
listG19 = cm.getoutput("ls " +dataPath+ "S10161313_" +inputdate+ "??0?.nc")
filesG19 = listG19.split("\n")

print "It was found " +str(len(filesG19))+ " G19 files!"


#-----Loop to verify if output file exists-------##
for pathFileG19 in filesG19:

    baseName = os.path.basename(pathFileG19)    
    currDate = baseName[10:22]
    hour = int(currDate[8:10])
    
    fileLW = folderBin+"/"+str(year)+"/"+str(month)+"/S11167039_"+currDate+".bin"
  

#------If file not exist executes solar radiation model------##
    if (os.path.isfile(fileLW)):
        print "File alredy exist for date: " +currDate

    else:
	if (hour == 0) or (hour == 3) or (hour == 6) or (hour == 9) or (hour == 12) or (hour == 15) or (hour == 18) or (hour == 21):
            print "Executing " +mainPath+ "/scripts/longWaveSouthAm.py " +currDate
	    os.system(mainPath+ "/scripts/longWaveSouthAm.py " +currDate)

            ## Convert binary to netcdf
            os.system(mainPath+ "/scripts/conv_bin2nc.sh "+currDate+" 7039")    
