#!/bin/bash
# 

#*************************************************************************\
# Copyright (c) 2019 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#  mainResolverStandstillISO230_2.bash
#
#  Created on: Oct 20, 2021
#      Author: anderssandstrom
#
#  Script for extracting and calculating statistics of resolver accuracy over one turn
#
#  Arguments:
#    1 Data file   (input)
#    2 Report file (output)
#    3 Test PV
#    4 Resolver PV
#    5 Resolver gain
#    6 Resolver offset
#    7 Motor Setpoint PV
#    8 Decimals
#    9 Unit
#
#*************************************************************************/

# Newline
nl='
'
if [ "$#" -ne 9 ]; then
   echo "mainResolverStandstill: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
TEST_PV=$3
RESOLVER_PV=$4
RESOLVER_GAIN=$5
RESOLVER_OFFSET=$6
MOTORSET_PV=$7
DEC=$8
UNIT=$9

TESTBASE=4000

# Finds out what position by reading setpoint
DATACOUNT_RESOLVER="10"
TESTCOUNT=8

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Resolver Performance"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT " ## Configuration"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Setting | Value |"
bash ecmcReport.bash $REPORT "--- | --- |"
bash ecmcReport.bash $REPORT "Data file | $FILE |"
bash ecmcReport.bash $REPORT "Resolver position source  | $RESOLVER_PV |"
bash ecmcReport.bash $REPORT "Resolver gain  | $RESOLVER_GAIN |"
bash ecmcReport.bash $REPORT "Resolver offset  | $RESOLVER_OFFSET |"
bash ecmcReport.bash $REPORT "Target position source  | $MOTORSET_PV |"
bash ecmcReport.bash $REPORT "Test number source  | $TEST_PV |"
bash ecmcReport.bash $REPORT "Unit  | $UNIT |"
bash ecmcReport.bash $REPORT ""

# Resolver 
bash ecmcReport.bash $REPORT "## Resolver reading over one turn"
bash ecmcReport.bash $REPORT "Measured at $TESTCOUNT positions offset by 45deg resolver shaft angle."
bash ecmcReport.bash $REPORT "The distrubution values are based on $DATACOUNT_RESOLVER values at each location."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Setpoint [$UNIT] | Resolver AVG[$UNIT] | Diff [$UNIT] | Resolver STD[$UNIT]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- | --- |"

TRIGGPV=$TEST_PV
DIFFS=""

for COUNTER in {1..8}
do
   # setpoint
   DATACOUNT="1"
   let "TRIGGVAL=$TESTBASE+$COUNTER"

   DATAPV=$MOTORSET_PV
   SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   echo "Setpoint=$SETPOINT"

   # resolver
   DATAPV=$RESOLVER_PV
   
   RESOLVER_VAL=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT_RESOLVER})
   RESOLVER_VAL=$(echo "$RESOLVER_VAL" | bash ecmcScaleOffsetLines.bash ${RESOLVER_GAIN} ${RESOLVER_OFFSET})
   RESOLVER_AVG=$(echo "$RESOLVER_VAL" | bash ecmcAvgLines.bash)
   RESOLVER_STD=$(echo "$RESOLVER_VAL" | bash ecmcStdLines.bash)
   DIFF_RESOLVER=$(echo "$RESOLVER_AVG-($SETPOINT)" | bc -l)
   DIFFS_RESOLVER+="$DIFF_RESOLVER "   
   echo "Resolver value AVG = $RESOLVER_AVG STD = $RESOLVER_STD"
   let "DEC_STD_AVG=$DEC+2"
   printf "%d | %.${DEC}f | %.${DEC_STD_AVG}f | %.${DEC_STD_AVG}f | %.${DEC_STD_AVG}f\n" $COUNTER $SETPOINT $RESOLVER_AVG $DIFF_RESOLVER $RESOLVER_STD >> $REPORT
done

MAX_RES_DIFF=$(echo "$DIFFS_RESOLVER" | bash ecmcAbsMaxDataRow.bash)
bash ecmcReport.bash $REPORT ""
printf "Resolver standstill error: %.${DEC_STD_AVG}f [$UNIT]\n" $MAX_RES_DIFF >> $REPORT
bash ecmcReport.bash $REPORT ""
