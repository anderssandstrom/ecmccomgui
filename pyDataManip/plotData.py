#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotCaMonitor.py [<filename>]")
  print ("example: python plotData.py xx.txt")
  print ("example stdin: cat data.log | grep -E 'thread|CPU' | python plotData.py" )
  print ("cat log.log | grep 'DIFF(ref-send)' | awk '{print $3}' | grep "-" | python ~/sources/ecmccomgui/pyDataManip/plotData.py")
def main():
  # Check args
  if len(sys.argv)>1:
    print(sys.argv[1] )
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
    dataFile=sys.stdin
 
  x=[]
  y=[]
  counter=0
  for line in dataFile:     
    print("LINE:" + line)
    x.append(counter)
    counter=counter+1
    y.append(float(line))
    
  plt.plot(x,y,'o-')
  #plt.legend(legend)
  plt.grid()
  #plt.title(fname)
  plt.xlabel("time")
  plt.show()
  
if __name__ == "__main__":
  main()
