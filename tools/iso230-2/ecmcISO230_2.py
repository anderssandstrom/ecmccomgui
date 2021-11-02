#!/usr/bin/python
# coding: utf-8

#*************************************************************************\
# Copyright (c) 2019 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#  ecmcISO230_2.py
#
#  Created on: Oct 20, 2021
#      Author: anderssandstrom
#
# Calculate ISO230-2 data
#
#*************************************************************************/

import sys
import numpy as np
import getpass
from datetime import datetime

## Example  input file:
#  # Input data file for ISO230-2 calcs derived from: /home/pi/sources/ecmc_bifrost_slits_sat/tests_2/11360/axis1/230_2_3.log
#  # variable definitions:
#  #     REF_PV                            : Variable name filter for reference position value.
#  #     TEST_PV                           : Variable name filter for test number.
#  #     TGT_SET_PV                        : Variable name filter for position setpoint.
#  #     UNIT                              : Unit for measurenments.
#  #     CYCLES                            : ISO230-2 cycle count (normally 5).
#  #     POSITIONS                         : ISO230-2 position count (normally 8).
#  #     DEC                               : Decimal count for printouts. 
#  #     TGT_DATA[<pos_id>]                : Target Position for <pos_id> (from TGT_SET_PV).
#  #     REF_DATA_FWD[<pos_id>,<cycle_id>] : Fwd. dir. ref system position for <pos_id> and <cycle_id> (from <REF_PV>).
#  #     REF_DATA_BWD[<pos_id>,<cycle_id>] : Bwd. dir. ref system position for <pos_id> and <cycle_id> (from <REF_PV>).
#  #
#  REF_PV=IOC_TEST:m0s005-Enc01-PosAct
#  TEST_PV=IOC_TEST:TestNumber
#  TGT_SET_PV=IOC_TEST:Axis1-PosSet
#  UNIT=mm
#  CYCLES=5
#  POSITIONS=5
#  DEC=5
#  TGT_DATA[1]=15
#  REF_DATA_FWD[1,1]=15.00474806227268489274
#  TGT_DATA[2]=25
#  REF_DATA_FWD[2,1]=24.99740135477538049142
#  TGT_DATA[3]=35
#  REF_DATA_FWD[3,1]=34.98964688373884069080
#  TGT_DATA[4]=45
#  REF_DATA_FWD[4,1]=44.99779519073248146343
#  TGT_DATA[5]=55
#  REF_DATA_FWD[5,1]=55.00268138941223904155
#  REF_DATA_FWD[1,2]=15.00474806227268489274
#  REF_DATA_FWD[2,2]=24.99842076362346898971
#  REF_DATA_FWD[3,2]=34.99250122851348848600
#  REF_DATA_FWD[4,2]=44.99840683604133456240
#  REF_DATA_FWD[5,2]=55.00288527118185674121
#  REF_DATA_FWD[1,3]=15.00495194404230259240
#  REF_DATA_FWD[2,3]=24.99740135477538049142
#  REF_DATA_FWD[3,3]=34.99331675559195928463
#  REF_DATA_FWD[4,3]=44.99881459958056996172
#  REF_DATA_FWD[5,3]=55.00696290657421073435
#  REF_DATA_FWD[1,4]=15.00637911642962649000
#  REF_DATA_FWD[2,4]=24.99821688185385129005
#  REF_DATA_FWD[3,4]=34.99413228267043008326
#  REF_DATA_FWD[4,4]=44.99840683604133456240
#  REF_DATA_FWD[5,4]=55.00573961595650453641
#  REF_DATA_FWD[1,5]=15.00678687996886188931
#  REF_DATA_FWD[2,5]=24.99862464539308668937
#  REF_DATA_FWD[3,5]=34.99331675559195928463
#  REF_DATA_FWD[4,5]=45.00024177196789385932
#  REF_DATA_FWD[5,5]=55.00288527118185674121
#  REF_DATA_BWD[1,1]=15.00067042688033089959
#  REF_DATA_BWD[2,1]=24.99964405424117518765
#  REF_DATA_BWD[3,1]=35.00024873575896107297
#  REF_DATA_BWD[4,1]=44.99779519073248146343
#  REF_DATA_BWD[5,1]=55.00288527118185674121
#  REF_DATA_BWD[1,2]=15.00168983572841939788
#  REF_DATA_BWD[2,2]=24.99964405424117518765
#  REF_DATA_BWD[3,2]=34.99290899205272388531
#  REF_DATA_BWD[4,2]=44.99942624488942306069
#  REF_DATA_BWD[5,2]=55.00084645348567974463
#  REF_DATA_BWD[1,3]=15.00209759926765479719
#  REF_DATA_BWD[2,3]=24.99862464539308668937
#  REF_DATA_BWD[3,3]=34.99719050921469557811
#  REF_DATA_BWD[4,3]=44.99820295427171686274
#  REF_DATA_BWD[5,3]=55.00716678834382843401
#  REF_DATA_BWD[1,4]=15.00393253519421409411
#  REF_DATA_BWD[2,4]=25.00005181778041058697
#  REF_DATA_BWD[3,4]=34.99963709045010797400
#  REF_DATA_BWD[4,4]=44.99881459958056996172
#  REF_DATA_BWD[5,4]=55.00818619719191693229
#  REF_DATA_BWD[1,5]=15.00332088988536099514
#  REF_DATA_BWD[2,5]=24.99923629070193978834
#  REF_DATA_BWD[3,5]=34.99535557328813628120
#  REF_DATA_BWD[4,5]=44.99657190011477526549
#  REF_DATA_BWD[5,5]=55.00043868994644434532

UNIT="UNIT="
CYCLES="CYCLES="
POSITIONS="POSITIONS"
TGT_DATA="TGT_DATA["
REF_DATA_FWD="REF_DATA_FWD["
REF_DATA_BWD="REF_DATA_BWD["
DEC="DEC="
REF_PV="REF_PV="
TEST_PV="TEST_PV="
TGT_SET_PV="TGT_SET_PV="

def printOutHelp():
  print ("python ecmcISO230_2.py <filename>]")
    
class ecmcISO230_2:
    def __init__(self):
        self.positions = 0
        self.cycles = 0
        self.refData_fwd = {}
        self.refData_bwd = {}
        self.tgtData = {}
        self.unit = ""
        self.decimals=4
        self.x_i_fwd={}
        self.x_i_fwd_avg={}
        self.x_i_bwd={}
        self.x_i_bwd_avg={}
        self.x_i_avg={}
        self.B_i={}
        self.B=0
        self.B_avg=0
        self.s_i_fwd={}
        self.s_i_bwd={}
        self.x_i_j_fwd={}
        self.x_i_j_bwd={}
        self.R_i_fwd={}
        self.R_i_bwd={}
        self.R_i={}
        self.R_fwd=0
        self.R_bwd=0
        self.E_fwd=0
        self.E_bwd=0
        self.E=0
        self.M=0
        self.A_fwd=0
        self.A_bwd=0
        self.A=0
        self.gearRatio=0
        self.offset=0
        self.refPosGrArray=np.array([])
        self.tgtPosGrArray=np.array([])
        self.fileName = ""
        self.tgtpv = "empty"
        self.refpv = "empty"
        self.testpv = "empty"

    # Load file. If fileName is empty then uses stdin
    def loadFile(self, fileName):
        self.fileName=fileName
        if len(fileName)==0:
            dataFile=sys.stdin
        else:
            dataFile=open(fileName,'r')

        # Parse data
        for line in dataFile:
            self.parseLine(line)

    # Execute all calcs
    def calcAll(self):
        self.calcX()
        self.calcB()
        self.calcS()
        self.calcR()
        self.calcE()
        self.calcM()
        self.calcA()

    # parse one line  of data
    def parseLine(self, line):
        if len(line.strip())==0:
            return

        # Ignore if "#"
        if line.strip()[0]=="#":
            return

        if line.find(UNIT)>=0:
            self.unit=line.split("=")[1].strip()
            return

        if line.find(CYCLES)>=0:
            self.cycles=int(line.split("=")[1])
            return

        if line.find(DEC)>=0:
            self.decimals=int(line.split("=")[1])
            return

        if line.find(POSITIONS)>=0:
            self.positions=int(line.split("=")[1])
            return

        if line.find(REF_PV)>=0:
            self.refpv=line.split("=")[1].strip()
            return

        if line.find(TEST_PV)>=0:
            self.testpv=line.split("=")[1].strip()
            return

        if line.find(TGT_SET_PV)>=0:
            self.tgtpv=line.split("=")[1].strip()
            return

        if line.find(REF_DATA_FWD)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            indexStr=indexStr.split("]")[0]
            i=int(indexStr.split(",")[0])
            j=int(indexStr.split(",")[1])
            self.refData_bwd[i,j]=float(line.split("=")[1])
            return

        if line.find(REF_DATA_BWD)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            indexStr=indexStr.split("]")[0]
            i=int(indexStr.split(",")[0])
            j=int(indexStr.split(",")[1])
            self.refData_fwd[i,j]=float(line.split("=")[1])
            return

        if line.find(TGT_DATA)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            i=int(indexStr.split("]")[0])
            self.tgtData[i]=float(line.split("=")[1])
            return

    def calcX(self):
        for i in range(1,self.positions+1):
          x_sum_fwd=0
          x_sum_bwd=0
          
          for j in range(1,self.cycles+1):
            #fwd
            self.x_i_j_fwd[i,j]=self.refData_fwd[i,j]-self.tgtData[i]
            x_sum_fwd+=self.x_i_j_fwd[i,j]
            #bwd
            self.x_i_j_bwd[i,j]=self.refData_bwd[i,j]-self.tgtData[i]
            x_sum_bwd+=self.x_i_j_bwd[i,j]

          self.x_i_fwd_avg[i]=x_sum_fwd/float(self.positions)
          self.x_i_bwd_avg[i]=x_sum_bwd/float(self.positions)
          self.x_i_avg[i]=(self.x_i_fwd_avg[i]+self.x_i_bwd_avg[i])/float(2)
          #print("X_fwd_avg[" +str(i) + "] = " + str(self.x_i_fwd_avg[i]))
          #print("X_bwd_avg[" +str(i) + "] = " + str(self.x_i_bwd_avg[i]))
          #print("X_avg[" +str(i) + "] = " + str(self.x_i_avg[i]))
          
    def calcB(self):
        B_sum=0
        for i in range(1,self.positions+1):
          # B
          self.B_i[i]=self.x_i_fwd_avg[i]-self.x_i_bwd_avg[i]
          B_sum+=self.B_i[i]
          if abs(self.B_i[i])>self.B:
              self.B=abs(self.B_i[i])
        
        self.B_avg=B_sum/float(self.positions)
        #print("B_avg = " + str(self.B_avg))
        #print("B = " + str(self.B))

    def calcS(self):
        for i in range(1,self.positions+1):
          s_fwd_tmp_sum=0
          s_bwd_tmp_sum=0  
          for j in range(1,self.cycles+1):
            #fwd
            s_fwd_tmp=(self.x_i_j_fwd[i,j]-self.x_i_fwd_avg[i])
            s_fwd_tmp=s_fwd_tmp*s_fwd_tmp
            s_fwd_tmp_sum+=s_fwd_tmp
            #bwd
            s_bwd_tmp=(self.x_i_j_bwd[i,j]-self.x_i_bwd_avg[i])
            s_bwd_tmp=s_bwd_tmp*s_bwd_tmp
            s_bwd_tmp_sum+=s_bwd_tmp

          self.s_i_fwd[i]=np.sqrt(s_fwd_tmp_sum/float(self.cycles-1))
          self.s_i_bwd[i]=np.sqrt(s_bwd_tmp_sum/float(self.cycles-1))
          #print("S_fwd[" +str(i) + "] = " + str(self.s_i_fwd[i]))
          #print("S_bwd[" +str(i) + "] = " + str(self.s_i_bwd[i]))

    def calcR(self):
        self.R_fwd=0
        self.R_bwd=0

        for i in range(1,self.positions+1):
          #fwd
          self.R_i_fwd[i]=4*self.s_i_fwd[i]
          if self.R_i_fwd[i]>self.R_fwd:
              self.R_fwd=self.R_i_fwd[i]
          #bwd
          self.R_i_bwd[i]=4*self.s_i_bwd[i]
          if self.R_i_bwd[i]>self.R_bwd:
              self.R_bwd=self.R_i_bwd[i]

          term1=2*self.s_i_fwd[i] + 2*self.s_i_bwd[i] + np.abs(self.B_i[i])
          term2=self.R_i_fwd[i]
          term3=self.R_i_bwd[i]
          termMax=term1
          if term2>termMax:
              termMax=term2
          if term3>termMax:
              termMax=term3
          self.R_i[i]=termMax

        self.R=self.R_fwd
        if self.R_fwd>self.R:
            self.R=self.R_fwd
            
        #print("R_fwd = "+ str(self.R_fwd))
        #print("R_bwd = "+ str(self.R_bwd))
        #print("R = "+ str(self.R))
          

    def calcE(self):
        x_i_avg_fwd_max=self.x_i_fwd_avg[1]
        x_i_avg_fwd_min=self.x_i_fwd_avg[1]
        x_i_avg_bwd_max=self.x_i_bwd_avg[1]
        x_i_avg_bwd_min=self.x_i_bwd_avg[1]
        for i in range(1,self.positions+1):
          #fwd
          if self.x_i_fwd_avg[i]>x_i_avg_fwd_max:
              x_i_avg_fwd_max=self.x_i_fwd_avg[i]
          if self.x_i_fwd_avg[i]<x_i_avg_fwd_min:
              x_i_avg_fwd_min=self.x_i_fwd_avg[i]

          #bwd
          if self.x_i_bwd_avg[i]>x_i_avg_bwd_max:
              x_i_avg_bwd_max=self.x_i_bwd_avg[i]
          if self.x_i_bwd_avg[i]<x_i_avg_bwd_min:
              x_i_avg_bwd_min=self.x_i_bwd_avg[i]
        
        self.E_fwd=x_i_avg_fwd_max-x_i_avg_fwd_min
        self.E_bwd=x_i_avg_bwd_max-x_i_avg_bwd_min

        x_i_avg_max=x_i_avg_fwd_max
        if x_i_avg_bwd_max>x_i_avg_max:
            x_i_avg_max=x_i_avg_bwd_max
        x_i_avg_min=x_i_avg_fwd_min
        if x_i_avg_bwd_min>x_i_avg_min:
            x_i_avg_min=x_i_avg_bwd_min
            
        self.E=x_i_avg_max-x_i_avg_min
        #print("E_fwd = " + str(self.E_fwd))
        #print("E_bwd = " + str(self.E_bwd))
        #print("E = " + str(self.E))

    def calcM(self):
        x_i_avg_max=self.x_i_avg[1]
        x_i_avg_min=self.x_i_avg[1]

        for i in range(1,self.positions+1):
          #fwd
          if self.x_i_avg[i]>x_i_avg_max:
            x_i_avg_max=self.x_i_avg[i]
          if self.x_i_avg[i]<x_i_avg_min:
            x_i_avg_min=self.x_i_avg[i]

        self.M=x_i_avg_max-x_i_avg_min
        #print("M = " + str(self.M))

    def calcA(self):
        term_max_fwd=self.x_i_fwd_avg[1]+2*self.s_i_fwd[1]
        term_min_fwd=self.x_i_fwd_avg[1]-2*self.s_i_fwd[1]
        term_max_bwd=self.x_i_bwd_avg[1]+2*self.s_i_bwd[1]
        term_min_bwd=self.x_i_bwd_avg[1]-2*self.s_i_bwd[1]

        for i in range(1,self.positions+1):
          #fwd
          term_temp_fwd_max=self.x_i_fwd_avg[i]+2*self.s_i_fwd[i]
          term_temp_fwd_min=self.x_i_fwd_avg[i]-2*self.s_i_fwd[i]
          if term_temp_fwd_max>term_max_fwd:
            term_max_fwd=term_temp_fwd_max
          if term_temp_fwd_min<term_min_fwd:
            term_min_fwd=term_temp_fwd_min
          #bwd
          term_temp_bwd_max=self.x_i_bwd_avg[i]+2*self.s_i_bwd[i]
          term_temp_bwd_min=self.x_i_bwd_avg[i]-2*self.s_i_bwd[i]
          if term_temp_bwd_max>term_max_bwd:
            term_max_bwd=term_temp_bwd_max
          if term_temp_bwd_min<term_min_bwd:
            term_min_bwd=term_temp_bwd_min
        
        self.A_fwd=term_max_fwd-term_min_fwd
        self.A_bwd=term_max_bwd-term_min_bwd

        term_max_max=term_max_fwd
        term_min_min=term_min_fwd
        if term_max_bwd>term_max_max:
            term_max_max=term_max_bwd
        if term_min_bwd<term_min_min:
            term_min_min=term_min_bwd
        self.A=term_max_max-term_min_min
        #print("A_fwd = " + str(self.A_fwd))
        #print("A_bwd = " + str(self.A_bwd))
        #print("A = " + str(self.A))
    
    def calcGearRatio(self):
        # Build arrays forward        
        self.dataPoints=0
        self.resError=0
        resError=0
        for i in range(1,self.positions+1):
          for j in range(1,self.cycles+1):      
            self.refPosGrArray=np.append(self.refPosGrArray,self.refData_fwd[i,j])
            self.tgtPosGrArray=np.append(self.tgtPosGrArray,self.tgtData[i])
            self.dataPoints+=1
 
        # Build arrays backward
        for i in range(1,self.positions+1):
          for j in range(1,self.cycles+1):      
            self.refPosGrArray=np.append(self.refPosGrArray,self.refData_bwd[i,j])
            self.tgtPosGrArray=np.append(self.tgtPosGrArray,self.tgtData[i])
            self.dataPoints+=1

        if len(self.tgtPosGrArray) == len(self.refPosGrArray) and len(self.refPosGrArray)>0:
          z, res, x, x, x = np.polyfit(self.refPosGrArray, self.tgtPosGrArray, 1, full=True)
          self.gearRatio=z[0]
          self.offset=z[1]
          self.resError=res[0]
        else:
          print ("Array size missmatch:")
          print ("L1: "+ str(len(self.refPosGrArray)) + " L2: " + str(len(fromArray)) )

        print(str(z[0])+ " " + str(z[1]) + " " + str(len(self.refPosGrArray)) + " "+ str(res[0]))
        return self.gearRatio, self.offset, self.dataPoints, self.resError

    def addUnit(self, start):
        return start + "[" + self.unit + "]"

    def addDataPointToTableRow(self, data):        
        return self.roundDataToStr(data)+ "|"

    def roundDataToStr(self, data):        
        return str(round(data,self.decimals))

    def reportInputDataMD(self):
        print("")
        print("## Input data")
        print("")
        print("### Data forward direction")
        print("")
        print("i = Position index []")
        print("")
        print("j = Cycle index []")
        print("")
        print("tgt_pos(i) = Target position at position i [" + self.unit + "]")
        print("")
        print("ref_pos(i,j) = Reference position at position i and cycle j [" + self.unit + "]")
        print("")

        # build table first row
        tableStr="i |"
        subStr="--- |"
        tableStr+=self.addUnit("tgt_pos(i) ") + "|"        
        subStr+="--- |"

        for j in range(1,self.cycles+1):
            tableStr += self.addUnit("ref_pos(i," + str(j)+ ") ") + "|"
            subStr+="--- |"
        print("")
        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(i)
          tempStr+=self.addDataPointToTableRow(self.tgtData[i])
          for j in range(1,self.cycles+1):
            tempStr+=self.addDataPointToTableRow(self.refData_fwd[i,j])
          print (tempStr)

        print("")
        print("### Data backward direction")
        print("")
        print("i = Position index []")
        print("")
        print("j = Cycle index []")
        print("")
        print("tgt_pos(i) = Target position at position i [" + self.unit + "]")
        print("")
        print("ref_pos(i,j) = Reference position at position i and cycle j [" + self.unit + "]")
        print("")

        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(i)
          tempStr+=self.addDataPointToTableRow(self.tgtData[i])          
          for j in range(1,self.cycles+1):            
            tempStr+=self.addDataPointToTableRow(self.refData_bwd[i,j])
          print (tempStr)
        print("")
    
    def reportInit(self):
        print("# ISO 230-2 motion test")
        print("")
        print("## Configuration")
        print("")
        print("### General")
        print("")
        print("Setting | Value")
        print("--- | --- |")
        if len(self.fileName)>0:
          print("Input file | " + self.fileName)
        else:
          print("Input file | sys.stdin")
        print("Time | " + str(datetime.now()))
        checkuser = getpass.getuser()
        print("User | " + checkuser)
        print("")
        print("### Cycle information")
        print("")
        print("Setting | Value")
        print("--- | --- |")
        print("Position count | " + str(self.positions) + " (i=1.." + str(self.positions)  + ")")
        print("Cycle count |" + str(self.cycles) + " (j=1.." + str(self.cycles)  + ")")
        print("Unit | " + self.unit)
        print("Reference position source | " + self.refpv)
        print("Target position source | " + self.tgtpv)
        print("Test number source | " + self.testpv)
        print("")

    def reportXB(self):
        print("")
        print("## ISO230-2 calculations:")        
        print("")
        print("### Positioning deviation and reversal error")
        print("")  
        print("#### Positioning deviation forward direction (unidirectional)")
        print("")
        print("x(i,j)   = Position deviation at position i, cycle j (reference position - target position) [" + self.unit + "]")
        print("")
        print("x_avg(i) = Mean unidirectional positioning deviation at a position")
        print("")

        # build table first row
        tableStr="i |"
        subStr="--- |"

        for j in range(1,self.cycles+1):            
            tableStr += self.addUnit("x(i,"+ str(j)+ ") ") + "|"
            subStr+="--- |"
        tableStr+=self.addUnit("x_avg(i)") + "|"
        subStr+="--- |"

        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(i)
          for j in range(1,self.cycles+1):
            tempStr+=self.addDataPointToTableRow(self.x_i_j_fwd[i,j])        
          tempStr+=self.addDataPointToTableRow(self.x_i_fwd_avg[i])
          print (tempStr)

        print("")
        print("#### Positioning deviation backward direction (unidirectional)")
        print("")
        print("x(i,j)   = Position deviation at position i, cycle j (reference position - target position) [" + self.unit + "]")
        print("")
        print("x_avg(i) = Mean unidirectional positioning deviation at a position")
        print("")

        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(i)
          for j in range(1,self.cycles+1):
            tableStr += str(i) + "|"
            tempStr+=self.addDataPointToTableRow(self.x_i_j_bwd[i,j])
          tempStr+=self.addDataPointToTableRow(self.x_i_bwd_avg[i])
          print (tempStr)

        print("")
        print("#### Positioning deviation bi-directional")
        print("")
        print("x_avg(i) = Mean bi-directional positioning deviation at a position[" + self.unit + "]")
        print("")
        print("B(i)     = Reversal error at a position [" + self.unit + "]")
        print("")

        # build table first row
        tableStr="i |"
        subStr="--- |"
        tableStr += self.addUnit("x_avg(i) ") + "|"
        subStr+="--- |"
        tableStr += self.addUnit("B(i) ") + "|"
        subStr+="--- |"        
        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(i)          
          tempStr+=self.addDataPointToTableRow(self.x_i_avg[i])        
          tempStr+=self.addDataPointToTableRow(self.B_i[i])
          print (tempStr)
        
        print("")
        print(self.addUnit("B = Axis reversal error "))
        print("")
        print(self.addUnit("B = " + self.roundDataToStr(self.B) + " "))
        print("")
        print(self.addUnit("B_avg = Axis avg. reversal error "))
        print("")
        print(self.addUnit("B_avg = " + self.roundDataToStr(self.B_avg) + " "))
        print("")

    def reportR(self):
      print("### Repeatability")
      print("")
      print(self.addUnit("S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position "))
      print("")
      print(self.addUnit("S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position "))
      print("")
      print(self.addUnit("R_fwd(i) = Forward unidirectional positioning repeatability at a position "))
      print("")
      print(self.addUnit("R_bwd(i) = Backward unidirectional positioning repeatability at a position "))
      print("")
      print(self.addUnit("R(i) = Bi-directional position repeatability at a position "))
      print("")

      # build table first row
      tableStr="i |"
      subStr="--- |"
      tableStr += self.addUnit("S_fwd(i) ") + "|"
      subStr+="--- |"
      tableStr += self.addUnit("S_bwd(i) ") + "|"
      subStr+="--- |"
      tableStr += self.addUnit("R_fwd(i) ") + "|"
      subStr+="--- |"
      tableStr += self.addUnit("R_bwd(i) ") + "|"
      subStr+="--- |"
      tableStr += self.addUnit("R(i) ") + "|"
      subStr+="--- |"
      print(tableStr)
      print(subStr)
      
      for i in range(1,self.positions+1): 
        tempStr=""
        tempStr+=self.addDataPointToTableRow(i)
        tempStr+=self.addDataPointToTableRow(self.s_i_fwd[i])
        tempStr+=self.addDataPointToTableRow(self.s_i_bwd[i])
        tempStr+=self.addDataPointToTableRow(self.R_i_fwd[i])
        tempStr+=self.addDataPointToTableRow(self.R_i_bwd[i])
        tempStr+=self.addDataPointToTableRow(self.R_i[i])
        print (tempStr)

      print("")
      print(self.addUnit("R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i))) "))
      print("")
      print(self.addUnit("R_fwd = " + self.roundDataToStr(self.R_fwd) + " "))
      print("")
      print(self.addUnit("R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i))) "))
      print("")
      print(self.addUnit("R_bwd = " + self.roundDataToStr(self.R_bwd) + " "))
      print("")
      print(self.addUnit("R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd)) "))
      print("")
      print(self.addUnit("R = " + self.roundDataToStr(self.R) + " " ))
      print("")

    def reportE(self):
      print("### Positioning Error")
      print("")
      print(self.addUnit("E_fwd = Forward unidirectional system positioning error of an axis "))
      print("")
      print(self.addUnit("E_fwd = " + self.roundDataToStr(self.E_fwd) + " "))
      print("")
      print(self.addUnit("E_bwd = Backward unidirectional system positioning error of an axis "))
      print("")
      print(self.addUnit("E_bwd = " + self.roundDataToStr(self.E_bwd) + " "))
      print("")
      print(self.addUnit("E = Bi-directional system positioning error of an axis "))
      print("")
      print(self.addUnit("E = " + self.roundDataToStr(self.E) + " "))
      print("")
      print(self.addUnit("M = Mean bi-directional system positioning error of an axis "))
      print("")
      print(self.addUnit("M = " + self.roundDataToStr(self.M) + " "))
      print("")

    def reportA(self):
      print("### Accuracy")
      print("")
      print(self.addUnit("A_fwd = Forward unidirectional accuracy of an axis "))
      print("")
      print(self.addUnit("A_fwd = " + self.roundDataToStr(self.A_fwd) + " "))
      print("")
      print(self.addUnit("A_bwd = Backward unidirectional accuracy of an axis "))
      print("")
      print(self.addUnit("A_bwd = " + self.roundDataToStr(self.A_bwd) + " "))
      print("")
      print(self.addUnit("A = Bi-directional accuracy of an axis "))
      print("")
      print(self.addUnit("A = " + self.roundDataToStr(self.A) + " "))
      print("")

    def reportMarkDown(self):
        self.reportInit()
        self.reportInputDataMD()
        self.reportXB()
        self.reportR()
        self.reportE()
        self.reportA()

def main():
  fname = "" 
  if len(sys.argv ) > 2  :  
      printOutHelp()
      sys.exit()

  if len(sys.argv)==2:
    fname=sys.argv[1]
    dataFile=open(fname,'r')

  if len(sys.argv)==1:
    dataFile=sys.stdin

  iso=ecmcISO230_2()
  
  #Load data (empty equals stdin)
  iso.loadFile(fname)

  # Calc process performance
  iso.calcAll()
  iso.reportMarkDown() 
   
if __name__ == "__main__":
  main()
