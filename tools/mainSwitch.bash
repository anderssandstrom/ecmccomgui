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
TRIGGVAL="2001"
DATAPV="IOC_TEST:Axis1-PosAct"
DATACOUNT="350"  # Must be enough to capture the switch transition
SWITCHPV="IOC_TEST:ec0-s2-EL1808-BI1"
SWITCHVAL=0
OPENLOOPVALS=""
RESOLVERVALS=""
COUNTER=0
DIFFS=""
# Engage
for TRIGGVAL in {2001..2010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "BWD switch engage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
done
# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD>> $REPORT
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
for TRIGGVAL in {2011..2020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "BWD switch disengage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f| %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD >> $REPORT
bash ecmcReport.bash $REPORT ""

############ HIGH LIMIT SWITCH
# Engage
SWITCHPV="IOC_TEST:ec0-s2-EL1808-BI2"
SWITCHVAL=0
RESOLVERVALS=""
OPENLOOPVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
COUNTER=0
DIFFS=""
bash ecmcReport.bash $REPORT "## High Limit Engage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]| Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |"

for TRIGGVAL in {4001..4010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "FWD switch engage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD >> $REPORT
bash ecmcReport.bash $REPORT ""

# Disengage
SWITCHVAL=1
RESOLVERVALS=""
OPENLOOPVALS=""
OPENLOOPAVG=""
RESOLVERAVG=""
COUNTER=0
DIFFS=""
bash ecmcReport.bash $REPORT "## Low Limit Disengage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Openloop [mm]| Resolver [mm]| Diff [mm]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |"

for TRIGGVAL in {4011..4020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV="IOC_TEST:Axis1-PosAct"
   OPENLOOPVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   OPENLOOPVALS+="$OPENLOOPVAL "
   DATAPV="IOC_TEST:ec0-s4-EL7211-Enc-PosAct"
   RESOLVERVAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   RESOLVERVAL=$(echo $RESOLVERVAL | bash ecmcScaleOffsetData.bash 1 ${RESOLVER_OFFSET})
   RESOLVERVALS+="$RESOLVERVAL "
   echo "FWD switch disengage position $TRIGGVAL: $OPENLOOPVAL, $RESOLVERVAL"
   DIFF=$(awk "BEGIN {print ($RESOLVERVAL-($OPENLOOPVAL))}")
   DIFFS+="$DIFF "
   printf "%d | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $COUNTER $OPENLOOPVAL $RESOLVERVAL $DIFF >> $REPORT
done

# Calc avg and std
OPENLOOPAVG=$(echo "$OPENLOOPVALS" | bash ecmcAvgDataRow.bash)
OPENLOOPSTD=$(echo "$OPENLOOPVALS" | bash ecmcStdDataRow.bash)
echo "Openloop AVG=$OPENLOOPAVG, STD=$OPENLOOPSTD" 
RESOLVERAVG=$(echo "$RESOLVERVALS" | bash ecmcAvgDataRow.bash)
RESOLVERSTD=$(echo "$RESOLVERVALS" | bash ecmcStdDataRow.bash)
DIFF_AVG=$(awk "BEGIN {print ($OPENLOOPAVG-($RESOLVERAVG))}")
DIFF_STD=$(awk "BEGIN {print ($OPENLOOPSTD-($RESOLVERSTD))}")
echo "Resolver AVG=$RESOLVERAVG, STD=$RESOLVERSTD"
printf "AVG | %.${DEC}f | %.${DEC}f | %.${DEC}f\n" $OPENLOOPAVG $RESOLVERAVG $DIFF_AVG >> $REPORT
printf "STD | %.${DEC}f | %.${DEC}f| %.${DEC}f\n" $OPENLOOPSTD $RESOLVERSTD $DIFF_STD >> $REPORT
bash ecmcReport.bash $REPORT ""
