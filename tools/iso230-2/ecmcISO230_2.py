#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np
import getpass
from datetime import datetime


## Example  input file:
# UNIT=mm
# CYCLES=5
# POSITIONS=5
# TGT_DATA[1]=15.00000
# TGT_DATA[2]=25.00000
# TGT_DATA[3]=35.00000
# TGT_DATA[4]=45.00000
# TGT_DATA[5]=55.00000
# REF_DATA_FWD[1,1]=15.00161 
# REF_DATA_FWD[2,1]=25.02160 
# REF_DATA_FWD[3,1]=34.99089
# REF_DATA_FWD[4,1]=44.96872
# REF_DATA_FWD[5,1]=55.02660 
# REF_DATA_FWD[1,2]=15.00161 
# REF_DATA_FWD[2,2]=25.02160 
# REF_DATA_FWD[3,2]=34.98946
# REF_DATA_FWD[4,2]=44.96811
# REF_DATA_FWD[5,2]=55.02619 
# REF_DATA_FWD[1,3]=15.00141 
# REF_DATA_FWD[2,3]=25.02120 
# REF_DATA_FWD[3,3]=34.99007
# REF_DATA_FWD[4,3]=44.96791
# REF_DATA_FWD[5,3]=55.02476 
# REF_DATA_FWD[1,4]=15.00181 
# REF_DATA_FWD[2,4]=25.02120 
# REF_DATA_FWD[3,4]=34.98987
# REF_DATA_FWD[4,4]=44.96771
# REF_DATA_FWD[5,4]=55.02558 
# REF_DATA_FWD[1,5]=15.00202 
# REF_DATA_FWD[2,5]=25.02099 
# REF_DATA_FWD[3,5]=34.98967 
# REF_DATA_FWD[4,5]=44.96811
# REF_DATA_FWD[5,5]=55.0255
# REF_DATA_BWD[1,1]=14.99876
# REF_DATA_BWD[2,1]=25.01468
# REF_DATA_BWD[3,1]=34.98743
# REF_DATA_BWD[4,1]=44.96689
# REF_DATA_BWD[5,1]=55.02598
# REF_DATA_BWD[1,2]=14.99896
# REF_DATA_BWD[2,2]=25.01529
# REF_DATA_BWD[3,2]=34.98681
# REF_DATA_BWD[4,2]=44.96628
# REF_DATA_BWD[5,2]=55.02558
# REF_DATA_BWD[1,3]=14.99937
# REF_DATA_BWD[2,3]=25.01488
# REF_DATA_BWD[3,3]=34.98661
# REF_DATA_BWD[4,3]=44.96669
# REF_DATA_BWD[5,3]=55.02578
# REF_DATA_BWD[1,4]=14.99917
# REF_DATA_BWD[2,4]=25.01448
# REF_DATA_BWD[3,4]=34.98783
# REF_DATA_BWD[4,4]=44.96689
# REF_DATA_BWD[5,4]=55.02537
# REF_DATA_BWD[1,5]=14.99896
# REF_DATA_BWD[2,5]=25.01468
# REF_DATA_BWD[3,5]=34.98804
# REF_DATA_BWD[4,5]=44.96567
# REF_DATA_BWD[5,5]=55.02517

UNIT="UNIT="
CYCLES="CYCLES="
POSITIONS="POSITIONS"
TGT_DATA="TGT_DATA["
REF_DATA_FWD="REF_DATA_FWD["
REF_DATA_BWD="REF_DATA_BWD["
DEC="DEC="

def printOutHelp():
  print ("python ecmcGearRatecmcISO230-2.py <filename>]")
    
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
          print("X_fwd_avg[" +str(i) + "] = " + str(self.x_i_fwd_avg[i]))
          print("X_bwd_avg[" +str(i) + "] = " + str(self.x_i_bwd_avg[i]))
          print("X_avg[" +str(i) + "] = " + str(self.x_i_avg[i]))
          
    def calcB(self):
        B_sum=0
        for i in range(1,self.positions+1):
          # B
          self.B_i[i]=self.x_i_fwd_avg[i]-self.x_i_bwd_avg[i]
          B_sum+=self.B_i[i]
          if abs(self.B_i[i])>self.B:
              self.B=abs(self.B_i[i])
        
        self.B_avg=B_sum/float(self.positions)
        print("B_avg = " + str(self.B_avg))
        print("B = " + str(self.B))

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
          print("S_fwd[" +str(i) + "] = " + str(self.s_i_fwd[i]))
          print("S_bwd[" +str(i) + "] = " + str(self.s_i_bwd[i]))

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
              self.R_bwd=self.R_i_fwd[i]

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
            
        print("R_fwd = "+ str(self.R_fwd))
        print("R_bwd = "+ str(self.R_bwd))
        print("R = "+ str(self.R))
          

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
        print("E_fwd = " + str(self.E_fwd))
        print("E_bwd = " + str(self.E_bwd))
        print("E = " + str(self.E))

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
        print("M = " + str(self.M))

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
        print("A_fwd = " + str(self.A_fwd))
        print("A_bwd = " + str(self.A_bwd))
        print("A = " + str(self.A))
    
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
        return str(round(data,self.decimals))+ "|"

    def reportInputDataMD(self):
        print("")
        print("## Data forward direction:")
        # build table first row
        tableStr=self.addUnit("Tgt pos ") + "|"        
        subStr="--- |"

        for j in range(1,self.cycles+1):
            tableStr += self.addUnit("Cycle " + str(j)+ " ") + "|"
            subStr+="--- |"
        print("")
        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(self.tgtData[i])          
          for j in range(1,self.cycles+1):            
            tempStr+=self.addDataPointToTableRow(self.refData_fwd[i,j])        
          print (tempStr)

        print("")
        print("## Data backward direction:")
        print("")
        print(tableStr)
        print(subStr)

        for i in range(1,self.positions+1): 
          tempStr=""
          tempStr+=self.addDataPointToTableRow(self.tgtData[i])          
          for j in range(1,self.cycles+1):            
            tempStr+=self.addDataPointToTableRow(self.refData_bwd[i,j])        
          print (tempStr)
        print("")
    
    def reportInit(self):
        print("# ISO 230-2 motion test")
        print("")
        #print("# ecmc motion performance report")
        #print("")
        #checkuser = getpass.getuser()
        #print("user: " + checkuser)
        #if len(self.fileName)>0:
        #  print("file: " + self.fileName)
        #else:
        #  print("file: sys.stdin")
        #print("time: " + str(datetime.now()))
        #print("")

    def reportMarkDown(self):
        self.reportInit()
        self.reportInputDataMD()

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
