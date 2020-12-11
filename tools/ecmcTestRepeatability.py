#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

homedPvSuffix='-homed'
testLoops = 10

if len(sys.argv)!=7:
  print("python ecmcTestRepeatability.py <motorPvNamepv> <testnumberpv> <from> <to> <velo> <testbasenum>")
  print("python ecmcTestRepeatability.py IOC:Axis1 IOC:TestNumber 0 100 25 3100")
  sys.exit()


motorPvName = sys.argv[1]
testPvname  = sys.argv[2]
motorHomedPvName = motorPvName + homedPvSuffix
fromPos = float(sys.argv[3])
toPos = float(sys.argv[4])
velo  = float(sys.argv[5]) 
testNumberBase = float(sys.argv[6]) 
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

maxPos = toPos
if fromPos > maxPos:
  maxPos = fromPos

minPos = fromPos
if toPos < minPos:
  minPos = toPos

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

while counter < testLoops:
  #run gap and center motorPvName to 0
  
  print ('Move axis to position ' + str(fromPos) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,fromPos,velo,timeOut)
  if not done:
    print (motorPvName + " failed to position.")
    sys.exit()
  timeOut = 5
  print ('Move axis to position ' + str(toPos) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,toPos,velo,timeOut)
  if not done:
    print( motorPvName + " failed to position.")
    sys.exit()
  counter = counter +1
  time.sleep(1)
  testPv.put(testNumberBase+counter)

time.sleep(1)
testPv.put(testNumberBase)

print("Test done!")
