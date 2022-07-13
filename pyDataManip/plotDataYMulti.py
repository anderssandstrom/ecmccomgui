#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser 
 
def printOutHelp():
  print ("python plotDatayMulti.py [file1] [file2] ...")
  print ("example: python plotDataYMulti.py file1.txt file2.txt ...")

def main():
  # Check args
  if len(sys.argv)>1:
    print (sys.argv[1] )
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)<2:  
      printOutHelp()
      sys.exit()
  filenames=[]
  files=[]
  i=0
  for arg in sys.argv:
    if i==0:
      i=i+1
      continue 
    filenames.append(sys.argv[i])
    files.append(open(sys.argv[i],'r'))
    i=i+1
   
  datasets=[]
  i=0
  for file in files:
    data=[]  
    counterX=0
    for line in file:
      print("LINE:" + line)
      if(len(line.strip())>0 and line.find(":") < 0 and line.find("/") < 0):        
        data.append(float(line))
        counterX=counterX+1
    i=i+1
    datasets.append(data)
  

  for data in datasets:
    plt.plot(data,'-')
    
  plt.grid()
  plt.show()
  
if __name__ == "__main__":
  main()
