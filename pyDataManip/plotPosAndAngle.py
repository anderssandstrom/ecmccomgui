#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotCaMonitor.py")
  

def main():
  # Check args
  if len(sys.argv)>1:    
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)!=3 and len(sys.argv)>1:  
      printOutHelp()
      sys.exit()
  
  pvY1name = "s013"
  pvY2name = "s014"
  pvY3name = "s015"
  pvY4name = "Rotation-PosAct"
    
  dataFile=sys.stdin

  parser=caMonitorArrayParser()
  pvY1=caPVArray(pvY1name)
  pvY2=caPVArray(pvY2name)
  pvY3=caPVArray(pvY3name)
  pvY4=caPVArray(pvY4name)
  
  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue

    #if line.find(pvY1name)==-1 and line.find(pvY2name)==-1:
    #  continue

    pvName, timeVal, data = parser.getValues(line)
    
    if pvName.find(pvY1name)>=0:
       pvY1.setValues(timeVal,data)
    if pvName.find(pvY2name)>=0:
       pvY2.setValues(timeVal,data)
    if pvName.find(pvY3name)>=0:
       pvY3.setValues(timeVal,data)
    if pvName.find(pvY4name)>=0:
       pvY4.setValues(timeVal,data)

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()
  y3Time,y3Data = pvY3.getData()
  y4Time,y4Data = pvY4.getData()

  print("Length of 1: " + str(len(y1Data)))
  print("Length of 2: " + str(len(y2Data)))
  print("Length of 3: " + str(len(y3Data)))
  print("Length of 4: " + str(len(y4Data)))
  fig, ax1 = plt.subplots()

  ax2 = ax1.twinx()
  print ("len: " + str(len(y1Data))+ " " + str(len(y2Data)))
  ax1.plot(y1Time, y1Data, 'o-b')
  ax1.plot(y2Time, y2Data, 'o-r')
  ax1.plot(y3Time, y3Data, 'o-g')
  ax1.legend(["Upper surface vertical","Horizontal","Lower surface vertical"])
  ax2.plot(y4Time, y4Data, 'o-k')
  ax2.legend(["Wheel angular position"])
  plt.grid()

  #plt.legend([pvY1name, pvY2name])
  plt.xlabel("time [s]")
  ax1.set_ylabel("Movement [mm]",color='k')
  ax2.set_ylabel("Angle [deg]",color='k')
  plt.show()
  
if __name__ == "__main__":
  main()
