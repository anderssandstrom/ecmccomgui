#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotData.py [<filename X>] [<filename Y>]")
  print ("example: python plotData.py xx.txt yy.txt")

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

  x=[]
  counterX=0
  for line in dataFileX:
    print("LINE:" + line)
    if(len(line.strip())>0 and line.find(":") < 0 and line.find("/") < 0):        
      x.append(float(line))
      counterX=counterX+1
  
  y=[]
  counterY=0
  for line in dataFileY:
    print("LINE:" + line)
    if(len(line.strip())>0 and line.find(":") < 0 and line.find("/") < 0):        
      y.append(float(line))
      counterY=counterY+1

  plt.plot(x,y,'o-')
  plt.grid()
  plt.show()
  
if __name__ == "__main__":
  main()
