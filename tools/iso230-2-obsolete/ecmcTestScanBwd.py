#!/usr/bin/env python
# Go to Fwd limit and then go back one mm and then again into the switch

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

homedPvSuffix='-Homed'
limitPvSuffix='-LimBwd'

testLoops = 10
timeout =50
if len(sys.argv)!=6:
  print("python ecmcTestScanBwd.py. <motorPvNamepv> <testnumberpv> <velo> <timeout> <testnumber>")
  print("python ecmcTestScanBwd.py IOC:Axis1 IOC:TestNumber 0.5 50 5000")
  sys.exit()


motorPvName = sys.argv[1]
testPvname  = sys.argv[2]
motorHomedPvName = motorPvName + homedPvSuffix
velo  = float(sys.argv[3]) 
timeout = float(sys.argv[4]) 
testNumber = float(sys.argv[5]) 
homedPv = epics.PV(motorHomedPvName)
testPv = epics.PV(testPvname)
limitPv=epics.PV(motorPvName+limitPvSuffix)
if limitPv is None:
   print ("Invalid limit pv") 
   sys.exit()

if testPv is None:
   print ("Invalid testPv") 
   sys.exit()
   
homed = homedPv.get()
#if not homed:
#   print ("Motor not homed. Test will abort.")
#   sys.exit()

testPv.put(testNumber)
startPos = ecmcSlitDemoLib.getActPos(motorPvName)
    
print ('Disable amplifier')
ecmcSlitDemoLib.setAxisEnable(motorPvName, 0)
time.sleep(.2) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motorPvName,1)

#Reset error on all axis
print ('Reset error axes.')
ecmcSlitDemoLib.setAxisReset(motorPvName, 1)
time.sleep(0.2)
ecmcSlitDemoLib.setAxisReset(motorPvName, 0)

print ('Enable amplifier')
ecmcSlitDemoLib.setAxisEnable(motorPvName, 1)
time.sleep(.2) #ensure that enabled goes down
error=ecmcSlitDemoLib.getAxisError(motorPvName,1)
counter = 0

print ('Move to switch')
error=ecmcSlitDemoLib.moveAxisVelocity(motorPvName,-velo,0)

polltime=1
wait_for_done = timeout
while wait_for_done > 0:
  time.sleep(polltime)
  limitVal = limitPv.get()
  if not limitVal:
      print ('Reached switch')
      wait_for_done = 0
  else: 
      wait_for_done-=polltime
      if wait_for_done==0:
          print ('Timeout! Did not reach switch..')
          sys.exit()

testPv.put(testNumber + 1)
print ('Now at switch')
