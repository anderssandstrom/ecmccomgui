#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotCaMonitor.py [<filename X>] [<filename Y>]")
  print ("example: python plotCaMonitor.py xx.txt yy.txt")

def main():
  # Check args
  if len(sys.argv)>1:
    print (sys.argv[1] )
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)!=3 and len(sys.argv)>1:  
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)==3:
    fnamex=sys.argv[1]
    dataFileX=open(fnamex,'r')

  if len(sys.argv)==3:
    fnamey=sys.argv[2]
    dataFileY=open(fnamey,'r')

  parserY=caMonitorArrayParser()

  firstY = 1
  for line in dataFileY:
    if not parserY.lineValid(line):
      continue
    
    pvName, timeVal, data=parserY.getValues(line)
    if firstY:    
      pvY=caPVArray(pvName)
      firstY = 0

    pvY.setValues(timeVal,data)    

  
  parserX=caMonitorArrayParser()
  firstX = 1  
  for line in dataFileX:
    if not parserX.lineValid(line):
      continue

    pvName, timeVal, data=parserX.getValues(line)
    if firstX:    
      pvX=caPVArray(pvName)
      firstX = 0

    pvX.setValues(timeVal,data)    
  
  timeSetX, dataSetX=pvX.getData()
  timeSetY, dataSetY=pvY.getData()

  plt.plot(dataSetX,dataSetY)
  #plt.legend("Amplitude []")
  plt.grid()
  #plt.title("FFT of 5Hz sin wave sampled at 100Hz (generated in ecmc PLC)")
  #plt.xlabel("Freq [Hz]")
  plt.show()
  
if __name__ == "__main__":
  main()
