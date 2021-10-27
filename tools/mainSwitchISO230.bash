#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
# Arg 3 Resolver offset
# Arg 4 Opto offset
# Arg 5 Decimals
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

# Newline
nl='
'
if [ "$#" -ne 5 ]; then
   echo "mainSwitch: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5

############ Limits #####################################################"

# Low limit
bash ecmcReport.bash $REPORT "# Limit Switch Performance"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Low Limit Engage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]| Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |"

# Get one openloop counter value just before BI1 0
TRIGGPV="IOC_TEST:TestNumber"
DATAPV="IOC_TEST:Axis1-PosAct"
DATACOUNT="350"  # Must be enough to capture the switch transition
SWITCHPV="IOC_TEST:m0s002-BI01"                   
SWITCHVAL=0
OPENLOOPVALS=""
RESOLVERVALS=""
COUNTER=0
DIFFS=""
RES_MIN=10000;
RES_MAX=-10000;
OPEN_MIN=10000;
OPEN_MAX=-10000;
# Engage
for TRIGGVAL in {3001..3010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:m0s004-Enc01-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "BWD switch engage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT

   if (( $(echo "$RESOLVERVAL > $RES_MAX" |bc -l) )); then
     RES_MAX=$RESOLVERVAL
   fi
   if (( $(echo "$RESOLVERVAL < $RES_MIN" |bc -l) )); then
     RES_MIN=$RESOLVERVAL
   fi
   if (( $(echo "$OPENLOOPVAL > $OPEN_MAX" |bc -l) )); then
     OPEN_MAX=$OPENLOOPVAL
   fi
   if (( $(echo "$OPENLOOPVAL < $OPEN_MIN" |bc -l) )); then
     OPEN_MIN=$OPENLOOPVAL
   fi

done
# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
RES_RANGE=$(echo "$RES_MAX-($RES_MIN)" | bc -l)
OPEN_RANGE=$(echo "$OPEN_MAX-($OPEN_MIN)" | bc -l)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD>> $REPORT
printf "Range | %.${DEC}f | %.${DEC}f\n" $OPEN_RANGE $RES_RANGE >> $REPORT

echo "RES_MIN=$RES_MIN, RES_MAX=$RES_MAX, RES_RANGE=$RES_RANGE"

bash ecmcReport.bash $REPORT ""

# Disengage
bash ecmcReport.bash $REPORT "## Low Limit Disengage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]| Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |"

SWITCHVAL=1
OPENLOOPVALS=""
RESOLVERVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
COUNTER=0
DIFFS=""
RES_MIN=10000;
RES_MAX=-10000;
OPEN_MIN=10000;
OPEN_MAX=-10000;

for TRIGGVAL in {3011..3020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:m0s004-Enc01-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "BWD switch disengage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
   if (( $(echo "$RESOLVERVAL > $RES_MAX" |bc -l) )); then
     RES_MAX=$RESOLVERVAL
   fi
   if (( $(echo "$RESOLVERVAL < $RES_MIN" |bc -l) )); then
     RES_MIN=$RESOLVERVAL
   fi
   if (( $(echo "$OPENLOOPVAL > $OPEN_MAX" |bc -l) )); then
     OPEN_MAX=$OPENLOOPVAL
   fi
   if (( $(echo "$OPENLOOPVAL < $OPEN_MIN" |bc -l) )); then
     OPEN_MIN=$OPENLOOPVAL
   fi

done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
RES_RANGE=$(echo "$RES_MAX-($RES_MIN)" |bc -l)
OPEN_RANGE=$(echo "$OPEN_MAX-($OPEN_MIN)" |bc -l)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f| %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD >> $REPORT
printf "Range | %.${DEC}f | %.${DEC}f\n" $OPEN_RANGE $RES_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""

############ HIGH LIMIT SWITCH
# Engage
SWITCHPV="IOC_TEST:m0s002-BI02"
SWITCHVAL=0
RESOLVERVALS=""
OPENLOOPVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
COUNTER=0
DIFFS=""
RES_MIN=10000;
RES_MAX=-10000;
OPEN_MIN=10000;
OPEN_MAX=-10000;

bash ecmcReport.bash $REPORT "## High Limit Engage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]| Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |"

for TRIGGVAL in {5001..5010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:m0s004-Enc01-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "FWD switch engage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
   if (( $(echo "$RESOLVERVAL > $RES_MAX" |bc -l) )); then
     RES_MAX=$RESOLVERVAL
   fi
   if (( $(echo "$RESOLVERVAL < $RES_MIN" |bc -l) )); then
     RES_MIN=$RESOLVERVAL
   fi
   if (( $(echo "$OPENLOOPVAL > $OPEN_MAX" |bc -l) )); then
     OPEN_MAX=$OPENLOOPVAL
   fi
   if (( $(echo "$OPENLOOPVAL < $OPEN_MIN" |bc -l) )); then
     OPEN_MIN=$OPENLOOPVAL
   fi
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
RES_RANGE=$(echo "$RES_MAX-($RES_MIN)" |bc -l)
OPEN_RANGE=$(echo "$OPEN_MAX-($OPEN_MIN)" |bc -l)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD >> $REPORT
printf "Range | %.${DEC}f | %.${DEC}f\n" $OPEN_RANGE $RES_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""

# Disengage
SWITCHVAL=1
RESOLVERVALS=""
OPENLOOPVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
COUNTER=0
DIFFS=""
RES_MIN=10000;
RES_MAX=-10000;
OPEN_MIN=10000;
OPEN_MAX=-10000;

bash ecmcReport.bash $REPORT "## High Limit Disengage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]| Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |"

for TRIGGVAL in {5011..5020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:m0s004-Enc01-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "FWD switch disengage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
   if (( $(echo "$RESOLVERVAL > $RES_MAX" |bc -l) )); then
     RES_MAX=$RESOLVERVAL
   fi
   if (( $(echo "$RESOLVERVAL < $RES_MIN" |bc -l) )); then
     RES_MIN=$RESOLVERVAL
   fi
   if (( $(echo "$OPENLOOPVAL > $OPEN_MAX" |bc -l) )); then
     OPEN_MAX=$OPENLOOPVAL
   fi
   if (( $(echo "$OPENLOOPVAL < $OPEN_MIN" |bc -l) )); then
     OPEN_MIN=$OPENLOOPVAL
   fi
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
RES_RANGE=$(echo "$RES_MAX-($RES_MIN)" |bc -l)
OPEN_RANGE=$(echo "$OPEN_MAX-($OPEN_MIN)" |bc -l)
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f| %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD >> $REPORT
printf "Range | %.${DEC}f | %.${DEC}f\n" $OPEN_RANGE $RES_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""
