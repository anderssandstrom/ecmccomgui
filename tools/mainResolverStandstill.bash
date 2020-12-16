#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
# Arg 3 Resolver offset
# Arg 4 Opto offset
# Arg 5 Decimals
# Arg 6 TestBase
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

# Newline
nl='
'
if [ "$#" -ne 6 ]; then
   echo "mainResolverStandstill: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5
TESTBASE=$6


# Finds out what position by reading setpoint
DATACOUNT_RESOLVER="75"
TESTCOUNT=8

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Resolver Value Distribution"

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Measured at $TESTCOUNT positions offset by 45deg resolver shaft angle. The distrubution values are based on $DATACOUNT_RESOLVER values at each location."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Setpoint [mm] | Resolver AVG[mm] | Resolver STD[mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- |"

TRIGGPV="IOC_TEST:TestNumber"
DIFFS=""

for COUNTER in {1..8}
do
   # setpoint
   DATACOUNT="1"
   let "TRIGGVAL=$TESTBASE+$COUNTER"

   DATAPV="IOC_TEST:Axis1-PosSet"
   SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   echo "Setpoint=$SETPOINT"

   # resolver
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   
   RESOLVER_VAL=$(bash ecmcGetLinesBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT_RESOLVER})
   RESOLVER_VAL=$(echo "$RESOLVER_VAL" | bash ecmcScaleOffsetLines.bash 1 ${RESOLVER_OFFSET})
   RESOLVER_AVG=$(echo "$RESOLVER_VAL" | bash ecmcAvgLines.bash)
   RESOLVER_STD=$(echo "$RESOLVER_VAL" | bash ecmcStdLines.bash)
   DIFF_RESOLVER=$(echo "$RESOLVER_VAL-$SETPOINT" | bc -l)
   DIFFS_RESOLVER+="$DIFF_RESOLVER "
   DIFF_MAX
   echo "Resolver value AVG = $RESOLVER_AVG STD = $RESOLVER_STD"
   let "DEC_STD_AVG=$DEC+2"
   printf "%d | %.${DEC}f | %.${DEC_STD_AVG}f | %.${DEC_STD_AVG}f | %.${DEC_STD_AVG}f\n" $COUNTER $SETPOINT $RESOLVER_AVG $DIFF_RESOLVER $RESOLVER_STD >> $REPORT
   #echo "DATA=$RESOLVER_VAL"
   #echo "$RESOLVER_VAL" | python ../pyDataManip/histCaMonitor.py
done

MAX_RES_DIFF=$(echo "$DIFFS_RESOLVER" | bash ecmcAbsMaxDataRow.bash)
bash ecmcReport.bash $REPORT ""
printf "Accuracy standstill (Resolver): %.${DEC}f\n" $MAX_RES_DIFF >> $REPORT
bash ecmcReport.bash $REPORT ""
