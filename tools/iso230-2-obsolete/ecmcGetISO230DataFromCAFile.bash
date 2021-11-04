#!/bin/bash
#*************************************************************************\
# Copyright (c) 2019 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#  ecmcGetISO230DataFromCAFile.bash
#
#  Created on: Oct 20, 2021
#      Author: anderssandstrom
#
# Get data from camonitor log file 
# Output in format suitable for iso230_2.py
#
#*************************************************************************/

# ALL args are mandatory
FILE=$1
CYCLES=$2
TESTS=$3
REFERENCEPV=$4
REF_GR=$5
REF_OFF=$6
TESTNUMPV=$7
MOTORSETPV=$8
UNIT=$9
DEC=${10}

# Input data file for ISO230-2 calcs.
# derived from
nl='
'

#     UNIT                              : Unit for measurenments (optional, defualts to mm).
#     CYCLES                            : ISO230-2 cycle count (optional, defaults to 5).
#     POSITIONS                         : ISO230-2 position count (optional, defaults to 8).
#     DEC                               : Decimal count for printouts (optional, defualts to 4). 


OUTPUTDATA="# Input data file for ISO230-2 calcs derived from: $FILE$nl"
OUTPUTDATA+="# Mandatory variable definitions:$nl"
OUTPUTDATA+="#     TGT_DATA[<pos_id>]                : Target Position for <pos_id> (from TGT_SET_PV).$nl"
OUTPUTDATA+="#     REF_DATA_FWD[<pos_id>,<cycle_id>] : Fwd. dir. ref system position for <pos_id> and <cycle_id> (from <REF_PV>).$nl"
OUTPUTDATA+="#     REF_DATA_BWD[<pos_id>,<cycle_id>] : Bwd. dir. ref system position for <pos_id> and <cycle_id> (from <REF_PV>).$nl"
OUTPUTDATA+="# Optional variable definitions:$nl"
OUTPUTDATA+="#     UNIT                              : Unit for measurenments (optional, defualts to mm).$nl"
OUTPUTDATA+="#     CYCLES                            : ISO230-2 cycle count (optional, defaults to 5).$nl"
OUTPUTDATA+="#     POSITIONS                         : ISO230-2 position count (optional, defaults to 8).$nl"
OUTPUTDATA+="#     DEC                               : Decimal count for printouts (optional, defualts to 4). $nl"
OUTPUTDATA+="#     REF_PV                            : Variable name filter for reference position value (optional).$nl"
OUTPUTDATA+="#     TEST_PV                           : Variable name filter for test number (optional).$nl"
OUTPUTDATA+="#     TGT_SET_PV                        : Variable name filter for position setpoint (optional).$nl"
OUTPUTDATA+="#$nl"
OUTPUTDATA+="REF_PV=$REFERENCEPV$nl"
OUTPUTDATA+="TEST_PV=$TESTNUMPV$nl"
OUTPUTDATA+="TGT_SET_PV=$MOTORSETPV$nl"
OUTPUTDATA+="UNIT=$UNIT$nl"
OUTPUTDATA+="CYCLES=$CYCLES$nl"
OUTPUTDATA+="POSITIONS=$TESTS$nl"
OUTPUTDATA+="DEC=$DEC$nl"

# Get forward direction data points (test numbers 1xx1..1xx)
TESTS=$(seq -w 1 1 $TESTS)
CYCLES=$(seq -w 1 1 $CYCLES)

# Forward DATA
TESTNUMBER_BASE=1
for CYCLE in $CYCLES;
do  
  for TEST in $TESTS
  do   
   TESTNUMBER=$TESTNUMBER_BASE$CYCLE"0"$TEST

   # Only write target positions once
   if (( $(echo "$CYCLE==1" | bc -l) )); then
      # Target position
     DATAPV=$MOTORSETPV
     TRIGGPV=$TESTNUMPV
     TRIGGVAL=$TESTNUMBER
     DATACOUNT=1
     DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})        
     TGT_DATA=$DATA     
     OUTPUTDATA+="TGT_DATA[$TEST]=$TGT_DATA$nl"
   fi

   # Reference
   DATAPV=$REFERENCEPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(bc -l <<< "$DATA*($REF_GR)+($REF_OFF)")
   REF_DATA=$DATA
   OUTPUTDATA+="REF_DATA_FWD[$TEST,$CYCLE]=$REF_DATA$nl"
  done
done

# Backward DATA
TESTNUMBER_BASE=2
for CYCLE in $CYCLES;
do  
  for TEST in $TESTS
  do   
   TESTNUMBER=$TESTNUMBER_BASE$CYCLE"0"$TEST

   # Reference
   DATAPV=$REFERENCEPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(bc -l <<< "$DATA*($REF_GR)+($REF_OFF)")
   REF_DATA=$DATA
   OUTPUTDATA+="REF_DATA_BWD[$TEST,$CYCLE]=$REF_DATA$nl"

  done
done
echo "$OUTPUTDATA "
