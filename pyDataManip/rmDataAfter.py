#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
from datetime import datetime
from caPVArrayLib import caPVArray
from caMonitorArrayParserLib import caMonitorArrayParser

def printOutHelp():    
  print "python rmDataAfter.py [<filename>] <time>"
  print "Remove data After a certain time."
  print "example: python rmDataAfter.py xx.txt '2019-05-16 08:51:25.869000' "
  print "example stdin: cat data.log | grep -E 'ActPos' | python rmDataAfter.py '2019-05-16 08:51:25.869000'" 

def main():
  timeLimit = ""
  # Check args
  if len(sys.argv)>1:
    print sys.argv[1] 
    pos1=sys.argv[1].find('-h')
    if(pos1>=0):
      printOutHelp()
      sys.exit()
  
  if (len(sys.argv)!=3 and len(sys.argv)!=2) and len(sys.argv)>1:  
      printOutHelp()
      sys.exit()
  
  if len(sys.argv)==3:      
    timeLimit = sys.argv[1]
    fname=sys.argv[2]
    dataFile=open(fname,'r')

  if len(sys.argv)==2:
    timeLimit = sys.argv[1]
    fname=""
    dataFile=sys.stdin;

  print "Using time limit: " + timeLimit

  parser=caMonitorArrayParser()
  parser.setHighTimeLimit(timeLimit)
  pvs=[]

  for line in dataFile:
    if not parser.lineValid(line):      
      continue

    pvName, timeVal, data=parser.getValues(line)
    newPv=True;
    pvToAddDataTo=caPVArray(pvName)
    # See if old or new pv
    for pv in pvs:
      if pv.getName() == pvName:        
        pvToAddDataTo=pv
        newPv=False;
        break;
    
    pvToAddDataTo.setValues(timeVal,data)
    if newPv:       
      pvs.append(pvToAddDataTo)
      print "Added PV: " + pvName
  
  
  legend=[]
  for pv in pvs:      
    pv.printValues()
  
if __name__ == "__main__":
  main()
