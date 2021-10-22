#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

homedPvSuffix='-Homed'
testLoops = 10

if len(sys.argv)!=8:
  print("python ecmcTestStepScan.py <motorPvNamepv> <testnumberpv> <startpos> <stoppos> <step> <velo> <testbasenum>")
  print("python ecmcTestStepScan.py IOC:Axis1 IOC:TestNumber 60 5 5 0.75 7100")
  sys.exit()


motorPvName = sys.argv[1]
testPvname  = sys.argv[2]
motorHomedPvName = motorPvName + homedPvSuffix
startpos = float(sys.argv[3])
stoppos = float(sys.argv[4])
stepsize = float(sys.argv[5])
velo  = float(sys.argv[6])
testNumberBase = float(sys.argv[7])
homedPv = epics.PV(motorHomedPvName)
testPv = epics.PV(testPvname)

if homedPv is None:
   print ("Invalid homed pv") 
   sys.exit()

if testPv is None:
   print ("Invalid testPv") 
   sys.exit()
   
homed = homedPv.get()
if not homed:
   print ("Motor not homed. Test will abort.")
   sys.exit()

if stepsize<=0:
   print ("Invalid stepsize.")
   sys.exit()

testPv.put(testNumberBase)

print ('Disable amplifier')
ecmcSlitDemoLib.setAxisEnable(motorPvName, 0)
time.sleep(0.2) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motorPvName,1)

#Reset error on all axis
print ('Reset error axes.')
ecmcSlitDemoLib.setAxisReset(motorPvName, 1)
time.sleep(0.2)
ecmcSlitDemoLib.setAxisReset(motorPvName, 0)

print ('Enable amplifier')
ecmcSlitDemoLib.setAxisEnable(motorPvName, 1)
time.sleep(0.2) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motorPvName,1)
counter = 0

timeOut = 50

pos = startpos
counter=0
done = False

if startpos>stoppos:
    done = pos < stoppos

if startpos<stoppos:
    done = pos > stoppos

while not done:
  print ('Move axis to position ' + str(pos))
  done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,pos,velo,timeOut)
  if not done:
    print (motorPvName + " failed to position.")
    sys.exit()
  timeOut = stepsize / velo * 2
  counter = counter + 1
  time.sleep(1)
  testPv.put(testNumberBase+counter)

  if startpos>stoppos:
    pos = pos - stepsize
    done = pos < stoppos
  if startpos<stoppos:    
    pos = pos + stepsize
    done = pos > stoppos

time.sleep(1)
testPv.put(testNumberBase)
print("Test done!")
