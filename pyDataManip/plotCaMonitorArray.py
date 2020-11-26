#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print "python plotCaMonitor.py [<filename>]"
  print "example: python plotCaMonitor.py xx.txt"
  print "example stdin: cat data.log | grep -E 'thread|CPU' | python plotCaMonitor.py" 

def main():
  # Check args
  if len(sys.argv)>1:
    print sys.argv[1] 
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)!=2 and len(sys.argv)>1:  
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)==2:
    fname=sys.argv[1]
    dataFile=open(fname,'r')

  if len(sys.argv)==1:
    fname=""
    dataFile=sys.stdin;

  parser=caMonitorArrayParser()
  pvs=[]
  dataBuffer=np.array([]);
  for line in dataFile:
    if not parser.lineValid(line):      
      continue

    pvName, timeVal, data=parser.getValues(line)
    dataBuffer=np.append(dataBuffer,data[:].astype(np.float))
  print dataBuffer  
  
  y=dataBuffer
  plt.plot(y)
  plt.legend("Data")
  plt.grid()
  plt.title("Raw data, sinus wave in 5Hz, (NFFT=1024)")
  plt.xlabel("time [samples in 100Hz]")
  plt.ylabel("[]")
  plt.show()
  
if __name__ == "__main__":
  main()
