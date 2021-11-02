#!/bin/bash
#*************************************************************************\
# Copyright (c) 2019 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#  mainISO230_2.bash
#
#  Created on: Dec 14, 2020
#      Author: anderssandstrom
#
#
# Main script for processing data for IS=230-2 SAT/FAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
#
# NOTE: Varaibles below needs to modified for each case:
#    MOTORACTPV             : Filter for motor open loop counter (actual position).
#    MOTORSETPV             : Filter for motor setpint position (or target position).
#    RESOLVER_PV             : Filter fir resolver actrual postion.
#    REFERENCE_PV            : Filter for referance position.
#    TESTNUM_PV              : Filter for testnumber.
#    DEC                    : Decimals in printouts.
#    UNIT                   : Unit for the position measurement.
#    ISO230_POS_COUNT       : ISO230-2 cycle position count.
#    ISO230_CYCLE_COUNT     : ISO230-2 cycle count.
#
#*************************************************************************/
#
# Data examples (camonitor):
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.529180 66.14321041  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.529180 1.527265625  
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.529180 1.527243125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.579143 66.12481403  
# IOC_TEST:m0s005-Enc01-PosAct   2021-10-27 09:04:48.579143 33.08044  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.579143 1.564765625  
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.579143 1.564743125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.629165 66.10466003  
# IOC_TEST:m0s005-Enc01-PosAct   2021-10-27 09:04:48.629165 2147.483643  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.629165 1.602265625  

if [ "$#" -ne 2 ]; then
   echo "main: Wrong arg count... Please specify input and output file."
   exit 1 
fi

##########################################################################
### Need to update these fileds for every FAT sat so everything is correct
##PV names:
MOTORACTPV="IOC_TEST:Axis1-PosAct"
MOTORSETPV="IOC_TEST:Axis1-PosSet"
RESOLVER_PV="IOC_TEST:m0s004-Enc01-PosAct"
REFERENCE_PV="IOC_TEST:m0s005-Enc01-PosAct"
TESTNUM_PV="IOC_TEST:TestNumber"
LOW_LIM_PV="IOC_TEST:m0s002-BI01"
HIGH_LIM_PV="IOC_TEST:m0s002-BI02"
# Number decimals in printouts
DEC=5
# Units for printouts
UNIT="mm"

# Defs for ISO230 analysis
ISO230_POS_COUNT=5
ISO230_CYCLE_COUNT=5

##########################################################################
# Below here NO variables should need to be updated/changed

FILE=$1
REPORT=$2

# Calculate gearratios based on this test (should be correct defined)
TESTNUM_GEARRATIO_FROM=1501
TESTNUM_GEARRATIO_TO=2501

# Newline
nl='
'
# Always 5 cycles in standard
# Get forward direction data points (test numbers 1xx1..1xx)
TESTS=$(seq -w 1 1 $ISO230_POS_COUNT)
CYCLES=$(seq -w 1 1 $ISO230_CYCLE_COUNT)

echo "Collect gear ratio data (only at test points in the matrix)...."
# GEAR_RATIO_DATA=$(bash mainCollectDataForGearRatioCalc.bash $FILE $ISO230_CYCLE_COUNT $ISO230_POS_COUNT)

## Init report file
bash ecmcReportInit.bash $REPORT $FILE

##### Gear Ratio ###################################################

# Use gear ratio python script to find gear ratios
echo "1. Calculate gear ratios..."

# Get ISO230-2 RESOLVER data from input file for calc of gear ratio (Collect data with GR=1 and OFFSET=0)
GEAR_RATIO_DATA_RESOLVER=$(bash ecmcGetISO230DataFromCAFile.bash $FILE $ISO230_CYCLE_COUNT $ISO230_POS_COUNT $RESOLVER_PV 1 0 $TESTNUM_PV $MOTORSETPV $UNIT $DEC)
#echo "$GEAR_RATIO_DATA_RESOLVER "
TEMP=$( echo "$GEAR_RATIO_DATA_RESOLVER " | python ecmcGearRatioISO230_2.py)
RES_GR=$(echo $TEMP | awk '{print $1}')
RES_OFF=$(echo $TEMP | awk '{print $2}')
RES_LEN=$(echo $TEMP | awk '{print $3}')
RES_ERR=$(echo $TEMP | awk '{print $4}')
echo "RES GR=$RES_GR, OFF=$RES_OFF, LEN=$RES_LEN, RESIDUAL=$RES_ERR"
RES_ERR_DISP=$(echo "scale=8;$RES_ERR/1.0" | bc -l)
RES_LEN_DISP=$(echo "scale=$DEC;$RES_LEN/1.0" | bc -l)
RES_GR_DISP=$(echo "scale=$DEC;$RES_GR/1.0" | bc -l)
RES_OFF_DISP=$(echo "scale=$DEC;$RES_OFF/1.0" | bc -l)

# Get ISO230-2 REFERENCE data from input file for calc of gear ratio (Collect data with GR=1 and OFFSET=0)
GEAR_RATIO_DATA_REFERENCE=$(bash ecmcGetISO230DataFromCAFile.bash $FILE $ISO230_CYCLE_COUNT $ISO230_POS_COUNT $REFERENCE_PV 1 0 $TESTNUM_PV $MOTORSETPV $UNIT $DEC)
#echo "$GEAR_RATIO_DATA_REFERENCE "
TEMP=$( echo "$GEAR_RATIO_DATA_REFERENCE " | python ecmcGearRatioISO230_2.py)
REF_GR=$(echo $TEMP | awk '{print $1}')
REF_OFF=$(echo $TEMP | awk '{print $2}')
REF_LEN=$(echo $TEMP | awk '{print $3}')
REF_ERR=$(echo $TEMP | awk '{print $4}')
echo "REF GR=$REF_GR, OFF=$REF_OFF, LEN=$REF_LEN, RESIDUAL=$REF_ERR"
REF_ERR_DISP=$(echo "scale=8;$REF_ERR/1.0" | bc -l)
REF_LEN_DISP=$(echo "scale=$DEC;$REF_LEN/1.0" | bc -l)
REF_GR_DISP=$(echo "scale=$DEC;$REF_GR/1.0" | bc -l)
REF_OFF_DISP=$(echo "scale=$DEC;$REF_OFF/1.0" | bc -l)

# Report gear ratios
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Gear Ratios"
bash ecmcReport.bash $REPORT "From | To | Ratio [] | Offset [$UNIT] | Data count [] | Residual error [$UNIT²]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- | --- | --- |"
bash ecmcReport.bash $REPORT "Target Position | Resolver | $RES_GR_DISP | $RES_OFF_DISP | $RES_LEN_DISP | $RES_ERR_DISP "
bash ecmcReport.bash $REPORT "Target Position | Reference | $REF_GR_DISP | $REF_OFF_DISP | $REF_LEN_DISP | $REF_ERR_DISP "
bash ecmcReport.bash $REPORT ""

##### ISO230-2 ###################################################
echo "2. ISO230-2 test..."
# Again Get ISO230-2 data from input file but with correct gear ratios and offset
TEST_DATA=$(bash ecmcGetISO230DataFromCAFile.bash $FILE $ISO230_CYCLE_COUNT $ISO230_POS_COUNT $REFERENCE_PV $REF_GR $REF_OFF $TESTNUM_PV $MOTORSETPV $UNIT $DEC)

#echo "TEST_DATA=$TEST_DATA "
# Calc ISO230-2 data
ISO230_OUTPUT=$( echo "$TEST_DATA " | python ecmcISO230_2.py)

# Add output from python to report
echo "$ISO230_OUTPUT " >> $REPORT
bash ecmcReport.bash $REPORT ""

##### Switches ##########################################################
echo "3. Limit switch test..."
# Use resolver since reference is out of range
bash mainSwitchISO230_2.bash $FILE $REPORT $TESTNUM_PV $RESOLVER_PV $RES_GR $RES_OFF $LOW_LIM_PV $HIGH_LIM_PV $DEC $UNIT

##### Resolver jitter ###################################################
echo "4. Resolver performance test..."
bash mainResolverStandstillISO230_2.bash $FILE $REPORT $RES_GR $RES_OFF $REF_GR $REF_OFF 5 4000

##### Finish ###################################################
echo "5. Report ready..."
