#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python ecmcGearRatioIgnoreTimeStamp.py <pv_from_filter> <pv_to_filter> <filename>]")
  print ("example: python ecmcGearRatio.py Axis1 5002 data.log")
  print ("example stdin: cat data.log | grep -E 'Axis1-ActPos | EL5002' | python ecmcGearRatio.py Axis1 5002" )
  print ("NOTE: data input must be sorted in increasing time since only data pairs with exactly the same timestamp will be used." )
  print ("Only use data for motion in a single direction, otherwise backlash can affect the gearratio." )
  print ("Ouputs z0 z1 datacount residual")
def main():
   
  if len(sys.argv ) > 4 or len(sys.argv) < 3  :  
      printOutHelp()
      sys.exit()

  fromPvNameFilter = sys.argv[1]
  toPvNameFilter = sys.argv[2]

#  print("Initiating calculation of gear ration between "+ fromPvNameFilter + " and " +toPvNameFilter)

  if len(sys.argv)==4:
    fname=sys.argv[3]
    dataFile=open(fname,'r')

  if len(sys.argv)==3:
    fname=""
    dataFile=sys.stdin

  parser=caMonitorArrayParser()  
  
  toArray=np.array([])
  fromArray=np.array([])
  fromTimeVal=0
  toTimeVal=0
  fromData=0
  toData=0

  for line in dataFile:
    if not parser.lineValid(line):      
      continue

    pvName, timeVal, data = parser.getValues(line)
  
    # Only allow pvs that comply to filter settings
    lineOK = 0
    if pvName.find(fromPvNameFilter) >= 0:
      fromPvName=pvName    
      fromData=data.astype( np.dtype('float64'))
      fromArray=np.append(fromArray,fromData)

    if pvName.find(toPvNameFilter) >= 0:
      toPvName=pvName
      toData=data.astype( np.dtype('float64'))
      toArray=np.append(toArray,toData)        
  
  if len(toArray) == len(fromArray) and len(fromArray)>0:
    z, res, x, x, x = np.polyfit(toArray, fromArray, 1, full=True)
  else:

    print ("Array size missmatch")
    print ("L1: "+ str(len(toArray)) + " L2: " + str(len(fromArray)) )
    sys.exit(1)
  
 # print("from *" + fromPvNameFilter + "* to *" + toPvNameFilter + "* [gear ratio, offset]: ")
  print(str(z[0])+ " " + str(z[1]) + " " + str(len(toArray)) + " "+ str(res[0]))

#  print("INVERTED!!! from *" + toPvNameFilter + "* to *" + fromPvNameFilter + "* [gear ratio, offset]: ")
#  z = np.polyfit(fromArray, toArray, 1)
#  print("INVERTED GR="+str(z))
  

if __name__ == "__main__":
  main()
