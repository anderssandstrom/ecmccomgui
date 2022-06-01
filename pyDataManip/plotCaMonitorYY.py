#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotCaMonitor.py <pvnameY1filter> <pvnameY2filter>")
  print ("example stdin: cat data.log | grep -E 'thread|CPU' | python plotCaMonitorYY.py EL3602 EL5021" )

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
      
  pvY1name=sys.argv[1]
  pvY2name=sys.argv[2]
    
  fname=""
  dataFile=sys.stdin

  parser=caMonitorArrayParser()
  pvY1=caPVArray(pvY1name)
  pvY2=caPVArray(pvY2name)

  for line in dataFile:
    
    if not parser.lineValid(line):      
      continue

    if line.find(pvY1name)==-1 and line.find(pvY2name)==-1:
      continue

    pvName, timeVal, data = parser.getValues(line)
    
    if pvName.find(pvY1name)>=0:
       pvY1.setValues(timeVal,data)
    if pvName.find(pvY2name)>=0:
       pvY2.setValues(timeVal,data)

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()

  print("Statistics: ")
  pvLength = pvY1.getLength()
  pvMax = np.max(y1Data)
  pvMin = np.min(y1Data)
  pvAvg = np.mean(y1Data)
  pvStd = np.std(y1Data)
  legStr = pvY1.getName() + "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  print (legStr)

  pvLength = pvY2.getLength()
  pvMax = np.max(y2Data)
  pvMin = np.min(y2Data)
  pvAvg = np.mean(y2Data)
  pvStd = np.std(y2Data)
  legStr = pvY2.getName() + "[" + str(pvLength) + "] " + str(pvMin) + ".." + str(pvMax) + ", mean: " + str(pvAvg) + ", std: " + str(pvStd)
  print (legStr)

  fig, ax1 = plt.subplots()

  ax2 = ax1.twinx()
  print ("len: " + str(len(y1Data))+ " " + str(len(y2Data)))
  ax1.plot(y1Time, y1Data, 'o-b')
  ax2.plot(y2Time, y2Data, 'o-g')
  plt.grid()
  #plt.legend([pvY1name, pvY2name])
  plt.xlabel("time [s]")
  ax1.set_ylabel(pvY1name,color='b')
  ax2.set_ylabel(pvY2name,color='g')
  plt.show()
  
if __name__ == "__main__":
  main()
