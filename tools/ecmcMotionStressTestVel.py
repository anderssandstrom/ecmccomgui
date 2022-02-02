#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
from random import *

if len(sys.argv)!=4:
  print("python ecmcMotionStressTestVel.py <motor_pv_prefix> <max_velo> <max_time>")
  print("python ecmcMotionStressTestVel.py IOC:Axis1 5 10")
  sys.exit()

# Some intressting PV:s:
#     IOC_TEST:Axis1-MtnCmd     // "MOVE_ABS", "MOVE_REL", "MOVE_VEL"
#     IOC_TEST:Axis1-MtnCmdData // Param to MtnCmd
#     IOC_TEST:Axis1-TgtPosCmd  // Target position
#     IOC_TEST:Axis1-TgtVelCmd  // Target Velocity
#     IOC_TEST:Axis1-EnaCmd     // Enable command
#     IOC_TEST:Axis1-EnaAct     // Enabled status
#     IOC_TEST:Axis1-ExeCmd     // Execute command
#     IOC_TEST:Axis1-RstCmd     // Reset command
#     IOC_TEST:Axis1-PosAct     // Actual position

# Suffixes:
exeCmdPvStr     = '-ExeCmd'
stpCmdPvStr     = '-StopCmd'
enaCmdPvStr     = '-EnaCmd'
enaActPvStr     = '-EnaAct'
tgtPosCmdPvStr  = '-TgtPosCmd'
tgtVelCmdPvStr  = '-TgtVelCmd'
mtnCmdPvStr     = '-MtnCmd'
mtnCmdDataPvStr = '-MtnCmdData'
posActPvStr     = '-PosAct'
rstCmdPvStr     = '-RstCmd'
errIdPvStr      = '-ErrId'

# Read args:
motorPrefix = sys.argv[1]
maxVelo      = float(sys.argv[2])
maxTime      = float(sys.argv[3])

# Link to PVs:
exeCmdPv     = epics.PV(motorPrefix + exeCmdPvStr)
stpCmdPv     = epics.PV(motorPrefix + stpCmdPvStr)
enaCmdPv     = epics.PV(motorPrefix + enaCmdPvStr)
enaActPv     = epics.PV(motorPrefix + enaActPvStr)
tgtPosCmdPv  = epics.PV(motorPrefix + tgtPosCmdPvStr)
tgtVelCmdPv  = epics.PV(motorPrefix + tgtVelCmdPvStr)
mtnCmdPv     = epics.PV(motorPrefix + mtnCmdPvStr)
mtnCmdDataPv = epics.PV(motorPrefix + mtnCmdDataPvStr)
posActPv     = epics.PV(motorPrefix + posActPvStr)
rstCmdPv     = epics.PV(motorPrefix + rstCmdPvStr)
errIdPv      = epics.PV(motorPrefix + errIdPvStr)

if exeCmdPv is None:
   print ("Invalid exeCmd pv") 
   sys.exit()

if stpCmdPv is None:
   print ("Invalid stpCmd pv") 
   sys.exit()

if enaCmdPv is None:
   print ("Invalid enaCmd pv") 
   sys.exit()

if enaActPv is None:
   print ("Invalid enaAct pv") 
   sys.exit()

if tgtPosCmdPv is None:
   print ("Invalid tgtPosCmd pv") 
   sys.exit()

if tgtVelCmdPv is None:
   print ("Invalid tgtVelCmd pv") 
   sys.exit()

if tgtVelCmdPv is None:
   print ("Invalid tgtVelCmd pv") 
   sys.exit()

if mtnCmdPv is None:
   print ("Invalid mtnCmd pv") 
   sys.exit()

if mtnCmdDataPv is None:
   print ("Invalid mtnCmdData pv") 
   sys.exit()

if posActPv is None:
   print ("Invalid posAct pv") 
   sys.exit()

if rstCmdPv is None:
   print ("Invalid rstCmd pv") 
   sys.exit()

if errIdPv is None:
   print ("Invalid errId pv") 
   sys.exit()

print ('Set motion mode to MOVE_ABS:')
mtnCmdPv.put('MOVE_VEL')
mtnCmdDataPv.put(0)

print ('Disable amplifier:')
enaCmdPv.put(0)
time.sleep(1) # Ensure that enabled goes down

# Reset error on all axis
print ('Reset error on axes (if any):')
rstCmdPv.put(1)
time.sleep(1)
rstCmdPv.put(0)

print ('Enable amplifier:')
enaCmdPv.put(1)
time.sleep(1)

waiting = 10
print('Waiting for enabled..')
while waiting > 0:
  if enaActPv.get():
      break
  print('...')
  time.sleep(0.1)
  waiting = waiting-1

if not enaActPv.get():
  printf('Failed to enable amplifier..')
  sys.exit(1)

counter = 1

stpCmdPv.put(0)

while 1:
  
  exeCmdPv.put(0)
  errorId = errIdPv.get()

  if errorId:
    print ('Axis in error state: ' + str(errorId))
    stpCmdPv.put(1)
    enaCmdPv.put(0)    
    sys.exit(1)

  # randomize a new target pos and velo
  newTgtVel = uniform(-maxVelo, maxVelo)  
  tgtVelCmdPv.put(newTgtVel)
  exeCmdPv.put(1)
  
  print ('Executing new motion cmd no. ' + str(counter) + ':')  
  print ('  Target velo:  ' + str(newTgtVel))
  timeToWait=uniform(0, maxTime)
  print ('  Time to wait: ' + str(timeToWait))
  time.sleep(timeToWait)
  
  counter = counter +1
