#!/usr/bin/env python

import epics
import os
import sys
import time
import math
import unittest
import ecmcSlitDemoLib
import numpy as np
# camonitor TARGET_DU:Rotation-ActPhaseErrorMM_Slow TARGET_DU:Rotation-ActTemp_Slow TARGET_DU:Rotation-ActTorque_Slow TARGET_DU:Rotation-ActVel_Slow TARGET_DU:Rotation-Brk-Temp1-Act-Slow TARGET_DU:Rotation-Brk-Temp2-Act-Slow TARGET_DU:Rotation-Brk-Torque-Cmd | tee data_x.log
print 'Starting simulation of startup Torque for Target wheel',

pvBrakeSetpointCmd = "TARGET_DU:Rotation-Brk-Torque-Cmd"
pvBrakeFreeWheelCmd = "TARGET_DU:Rotation-Brk-FreeWheelOn-Cmd"
pvVelAct = "TARGET_DU:Rotation-ActVel"
epics.caput(pvBrakeSetpointCmd, 0)
epics.caput(pvBrakeFreeWheelCmd, 1)

timeStep = 1
timePassed = 0
timePassedState2 = 0
runLoop = 1

state = 0 #Static traction state
nominalVel= 60.0/ (1.0 / 14.0 * 36.0)
# State 0 
torqueState0 = 80
#State 1
torqueState1Low = 50  # 0 rpm
torqueState1High = 100 # 23.33RPm
torqueState1K = (torqueState1High - torqueState1Low) / nominalVel
torqueState1M = torqueState1Low
# State 2 (x2 ramong down over 1h)
xArr=np.linspace(1,3600,3600)
state2TorqueArr=np.array([])
a = 100
b = -3.33e-2
c = 4.6296e-6  
for x in xArr:
  index=int(x)
  state2TorqueArr =  np.append( state2TorqueArr,a+b*x+c*x*x)
torqueSet = 0
epics.caput(pvBrakeSetpointCmd, torqueSet)
epics.caput(pvBrakeFreeWheelCmd, 0)
while runLoop:
  time.sleep(timeStep)
  print 'State: ' + str(state)
  timePassed = timePassed + 1
  actVel=epics.caget(pvVelAct)
  if state == 0:
    torqueSet = torqueState0
    if actVel>1:
      state = 1

  if state == 1: #Linear from 90Nm -> 160Nm (based on actvel)
    torqueSet=actVel*torqueState1K+torqueState1M
    if actVel>nominalVel:
      state = 2

  if state == 2: # Ramp down of torque from 160 to 100 in 60 minutes
    timePassedState2 = timePassedState2 + timeStep
    if timePassedState2 >3599:
      state = 3
      runLoop = 0
    else:       
      torqueSet = state2TorqueArr[int(timePassedState2)]
    
  print 'State: ' + str(state) + ' Troque: ' + str(torqueSet) + ' Time passes: ' +str(timePassed)
  epics.caput(pvBrakeSetpointCmd, torqueSet)



print 'Startup sequence simulation ended!'
sys.exit()



