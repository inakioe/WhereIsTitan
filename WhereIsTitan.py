#! /usr/bin/env python
"""
Created on Mon Jun  8 09:57:38 2015

@author: Inaki Ordonez-Etxeberria

Script to determine the coordinates of Titan in order to help the observation to the IDS Proposal SI2015a02 
"""
print 'The script shows the possition of Titan in order to help' 
print 'with the observation of IDS Proposal SI2015a02'
print 'USAGE: python WhereIsTitan.py ["YYYY/MM/DD hh:mm:ss"]'
import ephem
import sys
import numpy as np


def Rad2DegRA(ang):
    #To convert radian RA in to hh mm ss
    DegDec=(ang*180./np.pi)/15
    Deg=int(DegDec)
    Min=int((DegDec-Deg)*60)
    Sec=((((DegDec-Deg)*60)-Min)*60)    
    return Deg, Min, Sec
def Rad2DegDec(ang):
    #To convert radian DEC in to dd mm ss
    DegDec=(ang*180./np.pi)
    Deg=int(DegDec)
    Min=int((DegDec-Deg)*60)
    Sec=((((DegDec-Deg)*60)-Min)*60)    
    return Deg, abs(Min), abs(Sec)


try:
    date=str(sys.argv[1])
except IndexError:
    date='now'
#definition of the observatory
lat = '28.775867' #INT latitude
lon =  '-17.89733' #INT longitude
observatory = ephem.Observer()
observatory.lon = str(lon)
observatory.lat = str(lat)
observatory.elevation = 2400.0 #meters
#definition of the momemt of observation
if date  ==  'now':
    observatory.date = ephem.now()
else:
    observatory.date = ephem.Date(date)
print '                                                                         Saturn '     
print ' Date     Time(UTC)     RA          DEC                  AZ      ALT    distance|size' 
print '                                                                        (arcsec)' 
#Selecting Titan and Saturn
titan = ephem.Titan()
saturn = ephem.Saturn()
#Define the epoch
titan.epoch = ephem.J2000

sec2days=1.157408e-05
interval = 1800 #seconds

for i in xrange(0,12):
    if date == 'now':
        date = str(ephem.now())
        date2 = ephem.now() + (interval * sec2days)
    else:
        date2 = ephem.Date(date) + (interval * sec2days)
    #Computing the possition
    observatory.date=ephem.Date(date)
    titan.compute(observatory)
    saturn.compute(observatory)
    #Control colors
    #To show the limits of the observation depending of the altitude of Titan, with the limits of the INT
    if (titan.alt*180/np.pi < 20):
        cR = chr(27)+"[5;31m" #defininng color red
    elif (titan.alt*180/np.pi < 33):
        cR = chr(27)+"[0;33m" #defining color yellow
    else:
        cR =  chr(27)+"[0;98m"
    cW=  chr(27)+"[0m" #color white
    separation = (ephem.separation([titan.ra,titan.dec],saturn)*180/np.pi*3600)
    if separation < 3*(saturn.size):
        cS = chr(27)+"[5;36m" #defininng color red
    else:
        cS =  chr(27)+"[0;98m"
    [Ti_RaD,Ti_RaM,Ti_RaS] = Rad2DegRA(titan.ra) #Converts radians in hours.
    [Ti_DecD,Ti_DecM,Ti_DecS]= Rad2DegDec(titan.dec) #Converts radians in degrees.
    print cW, observatory.date, ': ', "%02d"%Ti_RaD, "%02d"%Ti_RaM, "%05.2f"%round(Ti_RaS,2),\
        "%02d"%Ti_DecD, "%02d"%Ti_DecM, "%05.2f"%round(Ti_DecS,2),'J2000  ',\
        "%06.2f"%round(titan.az*180/np.pi,2), cR, "%06.2f"%round(titan.alt*180/np.pi,2), cW, \
        cS, "%06.2f"%round(separation,2),cW, "%03.1f"%round(saturn.size,1) 
    date= str(ephem.Date(date2))
print ""
print "ALT in",chr(27)+"[0;31m", "RED:",chr(27)+"[0m", "out of the limit of the INT telescope."
print "ALT in",chr(27)+"[0;33m", "ORANGE:",chr(27)+"[0m", "raise the lower shutter."
print "Distance", chr(27)+"[0;36m","BLUE:",chr(27)+"[0m","Titan will be too much close to Saturn, less than 3 Saturn radii."

print ""
print "1.- Solar analog before observation: LAND107-684 15 37 18.1 -00 09 50 J2000 m=8.4"
print "2.- Solar analog after observation:  HD144585 16 07 03.3 -14 04 17 J2000 m=6.3"
print "3.- Find a suitable Spectrophotometric Standard Star at the same airmass"
print ""
    
