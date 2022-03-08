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
       print ("pvName: " + pvName + " pvY1name: " + pvY1name )    
    if pvName.find(pvY2name)>=0:
       pvY2.setValues(timeVal,data)
       print ("pvName: " + pvName + " pvY2name: " + pvY2name )
    

  print("Statistics: ")
  legend=[]

  y1Time,y1Data = pvY1.getData()
  y2Time,y2Data = pvY2.getData()

  fig, ax1 = plt.subplots()

  ax2 = ax1.twinx()
  print ("len: " + str(len(y1Data))+ " " + str(len(y2Data)))
  ax1.plot(y1Time, y1Data, 'o-b')
  ax2.plot(y2Time, y2Data, 'o-g')
  plt.grid()
  plt.xlabel("time [s]")
  ax1.set_ylabel(pvY1name)
  ax2.set_ylabel(pvY2name)
  plt.show()
  
if __name__ == "__main__":
  main()
