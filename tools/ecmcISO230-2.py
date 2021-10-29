#!/usr/bin/python
# coding: utf-8
import sys
import numpy as np

UNIT="UNIT="
CYCLES="CYCLES="
POSITIONS="POSITIONS"
TGT_DATA="TGT_DATA["
REF_DATA_FWD="REF_DATA_FWD["
REF_DATA_BWD="REF_DATA_BWD["

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

    def parseLine(self, line):
        print(line)
        if line.find(UNIT)>=0:
            self.unit=line.split("=")[1]
            print("UNIT!!!!!!!!")

            return

        if line.find(CYCLES)>=0:
            self.cycles=int(line.split("=")[1])
            print("CYCLES!!!!!!!!")
            return

        if line.find(POSITIONS)>=0:
            self.positions=int(line.split("=")[1])
            print("POSITIONS!!!!!!!!")
            return

        if line.find(REF_DATA_FWD)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            indexStr=indexStr.split("]")[0]
            i=int(indexStr.split(",")[0])
            j=int(indexStr.split(",")[1])
            self.refData_bwd[i,j]=float(line.split("=")[1])
            print("REFDATA_FWD!!!!!!!!")
            return

        if line.find(REF_DATA_BWD)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            indexStr=indexStr.split("]")[0]
            i=int(indexStr.split(",")[0])
            j=int(indexStr.split(",")[1])
            self.refData_fwd[i,j]=float(line.split("=")[1])
            print("REFDATA_BWD!!!!!!!!")
            return

        if line.find(TGT_DATA)>=0:
            indexStr=line.split("=")[0]
            indexStr=indexStr.split("[")[1]
            i=int(indexStr.split("]")[0])
            self.tgtData[i]=float(line.split("=")[1])
            print("TGT_DATA!!!!!!!!")
            return

    def calcX(self):
        for i in range(1,self.positions+1):
          x_sum_fwd=0
          x_sum_bwd=0
          
          for j in range(1,self.cycles+1):
            #fwd
            self.x_i_j_fwd[i,j]=self.refData_fwd[i,j]-self.tgtData[i]
            self.x_i_fwd[i,j]=self.x_i_j_fwd[i,j]
            x_sum_fwd+=self.x_i_j_fwd[i,j]
            #bwd
            self.x_i_j_bwd[i,j]=self.refData_bwd[i,j]-self.tgtData[i]
            self.x_i_bwd[i,j]=self.x_i_j_bwd[i,j]
            x_sum_bwd+=self.x_i_j_bwd[i,j]

          self.x_i_fwd_avg[i]=x_sum_fwd/self.positions
          self.x_i_bwd_avg[i]=x_sum_bwd/self.positions
          self.x_i_avg[i]=(self.x_i_fwd_avg[i]+self.x_i_bwd_avg[i])/2 
          
    def calcB(self):
        B_sum=0
        for i in range(1,self.positions+1):
          # B
          self.B_i[i]=self.x_i_fwd_avg[i]-self.x_i_bwd_avg[i]
          B_sum+=self.B_i[i]
          if abs(self.B_i[i])>self.B:
              self.B=abs(self.B_i[i])
        
        self.B_avg=B_sum/self.positions

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

          self.s_i_fwd[i]=np.sqrt(s_fwd_tmp_sum/(self.cycles-1))
          self.s_i_bwd[i]=np.sqrt(s_bwd_tmp_sum/(self.cycles-1))

    def calcR(self):
        for i in range(1,self.positions+1):
          #fwd
          self.R_i_fwd[i]=4*self.s_i_fwd[i]
          #bwd
          self.R_i_bwd[i]=4*self.s_i_bwd[i]

def main():
   
  if len(sys.argv ) > 2  :  
      printOutHelp()
      sys.exit()

  if len(sys.argv)==2:
    fname=sys.argv[1]
    dataFile=open(fname,'r')

  if len(sys.argv)==3:
    fname=""
    dataFile=sys.stdin

  iso=ecmcISO230_2()

  for line in dataFile:
      iso.parseLine(line)
  iso.calcX()
  iso.calcB()
  iso.calcS()
   
if __name__ == "__main__":
  main()
