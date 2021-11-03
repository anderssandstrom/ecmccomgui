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

testLoops = 10

if len(sys.argv)!=4:
  print("python ecmcTestMovePos.py <motorPvNamepv> <pos> <velo>")
  print("python ecmcTestMovePos.py IOC:Axis1 10 5")
  sys.exit()


motorPvName = sys.argv[1]
pos = float(sys.argv[2])
velo  = float(sys.argv[3]) 
 
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

timeOut = 5
startPos = ecmcSlitDemoLib.getActPos(motorPvName)
timeOut = abs(startPos-pos)/velo
print ('Move axis to position: ' + str(pos))
done=ecmcSlitDemoLib.moveAxisPosition(motorPvName,pos,velo,timeOut)
