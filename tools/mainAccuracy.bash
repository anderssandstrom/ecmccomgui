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
TESTCOUNT=12

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Accuracy based on resolver and micro epsilon sensor"

# Resolver 
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Measured at $TESTCOUNT positions offset by 5mm over the entire actuator stroke."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Setpoint [mm] | Resolver [mm] | Micro Epsilon [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- |"

TRIGGPV="IOC_TEST:TestNumber"
DIFFS=""
DATACOUNT="1"

for COUNTER in {1..12}
do
   let "TRIGGVAL=$TESTBASE+$COUNTER"

   # setpoint   
   DATAPV="IOC_TEST:Axis1-PosSet"
   SETPOINT=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   echo "Setpoint=$SETPOINT"

   # resolver
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"   
   RESOLVER_VAL=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   RESOLVER_VAL=$(echo "$RESOLVER_VAL" | bash ecmcScaleOffsetLines.bash 1 ${RESOLVER_OFFSET})
   echo "Resolver value = $RESOLVER_VAL"
   
   # opto
   DATAPV="IOC_TEST:ec0-s5-OptoILD2300_50mm-AI1"
   OPTO_VAL=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})
   OPTO_VAL=$(echo $OPTO_VAL | bash ecmcScaleOffsetData.bash -1 ${OPTO_OFFSET})
   # Ensure value is valid (>0)
   if (( $(echo "$OPTO_VAL < 0.0" | bc -l) )); then
      OPTO_VAL="Out of range"
      printf "%d | %.${DEC}f | %.${DEC}f | %s\n" $COUNTER $SETPOINT $RESOLVER_VAL "$OPTO_VAL" >> $REPORT
   else
      printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $SETPOINT $RESOLVER_VAL $OPTO_VAL >> $REPORT
   fi

   echo "Opto value =$OPTO_VAL"
   
done
