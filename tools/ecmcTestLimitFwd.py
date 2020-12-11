#!/usr/bin/env python
# Go to Fwd limit and then go back one mm and then again into the switch

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib

testNumberBase=2100
homedPvSuffix='-homed'
limitPvSuffix='-limitfwd'

testLoops = 10

if len(sys.argv)!=5:
  print("python ecmcTestLimitFwd.py.py <motorPvNamepv> <testnumberpv> <stepsize> <velo>")
  print("python ecmcTestLimitFwd.py.py IOC:Axis1 IOC:TestNumber 1 0.5")
  sys.exit()


motorPvName = sys.argv[1]
testPvname  = sys.argv[2]
motorHomedPvName = motorPvName + homedPvSuffix
stepSize = float(sys.argv[3])
velo  = float(sys.argv[4]) 
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

testPv.put(testNumberBase)
startPos = ecmcSlitDemoLib.getActPos(motorPvName)
hepp = input('Start data acquisition now. Push enter when ready.\n')
    
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


print ('Move to switch')
error=ecmcSlitDemoLib.moveAxisVelocity(motorPvName,velo)

timeout = 50
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

timeOut = 5
startPos = ecmcSlitDemoLib.getActPos(motorPvName)-stepSize  # Now in the limit
print ('Move axis to position startposition just before switch: ' + str(startPos))
done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,startPos,velo,timeOut)

while counter < testLoops:
  print ('Engage switch' + str(startPos+stepSize) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,startPos+stepSize,velo,timeOut)
  if not done:
    print (motorPvName + " failed to position.")
    sys.exit()
  counter = counter + 1
  time.sleep(1)
  testPv.put(testNumberBase+counter)

  print ('Disengage switch' + str(startPos) + ' (cycles = ' + str(counter) + ').')
  done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,startPos,velo,timeOut)
  if not done:
    print (motorPvName + " failed to position.")
    sys.exit()

  time.sleep(1)
  testPv.put(testNumberBase+testLoops)

time.sleep(1)
testPv.put(testNumberBase)

print("Test done!")
