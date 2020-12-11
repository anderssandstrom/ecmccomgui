#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

testNumberBase=1000
homedPvSuffix='-homed'


if len(sys.argv)!=7:
  print("python ecmcTestResolver.py <motorPvNamepv> <testnumberpv> <stepsize> <steps> <velo> <testbasenumber>")
  print("python ecmcTestResolver.py IOC:Axis1 IOC:TestNumber 0.125 8 0.25 1000")
  sys.exit()


motorPvName = sys.argv[1]
testPvname  = sys.argv[2]
motorHomedPvName = motorPvName + homedPvSuffix
stepSize = float(sys.argv[3])
steps = float(sys.argv[4])
velo  = float(sys.argv[5])
testNumberBase = float(sys.argv[6])
homedPv = epics.PV(motorHomedPvName)
testPv = epics.PV(testPvname)

#if homedPv is None:
#   print ("Invalid homed pv") 
#   sys.exit()

if testPv is None:
   print ("Invalid testPv") 
   sys.exit()
   
homed = homedPv.get()
#if not homed:
#   print ("Motor not homed. Test will abort.")
#   sys.exit()

testPv.put(testNumberBase)
startPos = ecmcSlitDemoLib.getActPos(motorPvName)+1
    
print ('Disable amplifier')
ecmcSlitDemoLib.setAxisEnable(motorPvName, 0)
time.sleep(1) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motorPvName,1)

#Reset error on all axis
print ('Reset error axes.')
ecmcSlitDemoLib.setAxisReset(motorPvName, 1)
time.sleep(0.5)
ecmcSlitDemoLib.setAxisReset(motorPvName, 0)

print ('Enable amplifier')
ecmcSlitDemoLib.setAxisEnable(motorPvName, 1)
time.sleep(1) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motorPvName,1)
counter = 0

timeOut = 2

while counter < steps:
  #run gap and center motorPvName to 0
  counter = counter + 1
  print ('Move axis to position ' + str(startPos+counter*stepSize) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,startPos+counter*stepSize,velo,timeOut)
  if not done:
    print (motorPvName + " failed to position.")
    sys.exit()
  time.sleep(1)
  testPv.put(testNumberBase+counter)

time.sleep(1)
testPv.put(testNumberBase)

print("Test done!")
