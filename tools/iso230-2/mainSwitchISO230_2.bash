#!/bin/bash
# 

#*************************************************************************\
# Copyright (c) 2019 European Spallation Source ERIC
# ecmc is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#
#  mainSwitchISO230_2.bash
#
#  Created on: Oct 20, 2021
#      Author: anderssandstrom
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
# Arg 3 TEST_PV
# Arg 4 REF_PV
# Arg 5 REF gain
# Arg 6 REF offset
# Arg 7 LOW_LIM_PV 
# Arg 8 HIGH_LIM_PV
# Arg 9 Decimals
# Arg 10 Unit
#*************************************************************************/

# Newline
nl='
'
if [ "$#" -ne 10 ]; then
   echo "mainSwitch: Wrong arg count... Please specify correct input args."
   exit 1 
fi

FILE=$1
REPORT=$2
TEST_PV=$3
REF_PV=$4
REF_GR=$5
REF_OFF=$6
LOW_LIM_PV=$7
HIGH_LIM_PV=$8
DEC=$9
UNIT=${10}

############ Limits #####################################################"

# Low limit
bash ecmcReport.bash $REPORT "# Limit Switch Performance"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT " ## Configuration"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Setting | Value |"
bash ecmcReport.bash $REPORT "--- | --- |"
bash ecmcReport.bash $REPORT "Data file | $FILE |"
bash ecmcReport.bash $REPORT "Unit  | $UNIT |"
bash ecmcReport.bash $REPORT "Reference position source  | $REF_PV |"
bash ecmcReport.bash $REPORT "Low Limit source  | $LOW_LIM_PV |"
bash ecmcReport.bash $REPORT "High Limit source  | $HIGH_LIM_PV |"
bash ecmcReport.bash $REPORT "Test number source  | $TEST_PV |"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Low Limit Engage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Reference [$UNIT] "
bash ecmcReport.bash $REPORT "--- | --- |"

# Get one reference value just before BI1 0
TRIGGPV=$TEST_PV
DATACOUNT="400"  # Must be enough to capture the switch transition
SWITCHPV=$LOW_LIM_PV
SWITCHVAL=0
REF_VALS=""
COUNTER=0
DIFFS=""
# this is uggly...
REF_MIN=10000;
REF_MAX=-10000;
# Engage
for TRIGGVAL in {3001..3010}
do
   let "COUNTER=$COUNTER+1"   
   DATAPV=$REF_PV
   REF_VAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL=$(echo $REF_VAL | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS+="$REF_VAL "
   echo "BWD switch engage position $TRIGGVAL: $REF_VAL"
   
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL >> $REPORT

   if (( $(echo "$REF_VAL > $REF_MAX" | bc -l) )); then
     REF_MAX=$REF_VAL
   fi
   if (( $(echo "$REF_VAL < $REF_MIN" | bc -l) )); then
     REF_MIN=$REF_VAL
   fi

done

# Calc avg and std
REF_AVG=$(echo "$REF_VALS" | bash ecmcAvgDataRow.bash)
REF_STD=$(echo "$REF_VALS" | bash ecmcStdDataRow.bash)
REF_RANGE=$(echo "$REF_MAX-($REF_MIN)" | bc -l)
echo "Resference AVG=$REF_AVG, STD=$REF_STD"
printf "AVG | %.${DEC}f | \n" $REF_AVG >> $REPORT
printf "STD | %.${DEC}f | \n" $REF_STD >> $REPORT
printf "Range | %.${DEC}f\n"  $REF_RANGE >> $REPORT

echo "REF_MIN=$REF_MIN, REF_MAX=$REF_MAX, REF_RANGE=$REF_RANGE"

bash ecmcReport.bash $REPORT ""

# Disengage
bash ecmcReport.bash $REPORT "## Low Limit Disengage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Reference [$UNIT] "
bash ecmcReport.bash $REPORT "--- | --- |"

SWITCHVAL=1
REF_VALS=""
REF_AVG=""
COUNTER=0
REF_MIN=10000;
REF_MAX=-10000;

for TRIGGVAL in {3011..3020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV=$REF_PV
   REF_VAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL=$(echo $REF_VAL | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS+="$REF_VAL "
   echo "BWD switch disengage position $TRIGGVAL: $REF_VAL"
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL >> $REPORT
   if (( $(echo "$REF_VAL > $REF_MAX" |bc -l) )); then
     REF_MAX=$REF_VAL
   fi
   if (( $(echo "$REF_VAL < $REF_MIN" |bc -l) )); then
     REF_MIN=$REF_VAL
   fi
done

# Calc avg and std
REF_AVG=$(echo "$REF_VALS" | bash ecmcAvgDataRow.bash)
REF_STD=$(echo "$REF_VALS" | bash ecmcStdDataRow.bash)
REF_RANGE=$(echo "$REF_MAX-($REF_MIN)" |bc -l)
echo "Reference AVG=$REF_AVG, STD=$REF_STD"
printf "AVG | %.${DEC}f |\n" $REF_AVG >> $REPORT
printf "STD | %.${DEC}f |\n" $REF_STD >> $REPORT
printf "Range | %.${DEC}f |\n" $REF_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""


############ HIGH LIMIT SWITCH
# Engage
SWITCHPV=$HIGH_LIM_PV
SWITCHVAL=0
REF_VALS=""
REF_AVG=""
COUNTER=0
DIFFS=""
REF_MIN=10000;
REF_MAX=-10000;

bash ecmcReport.bash $REPORT "## High Limit Engage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Reference [$UNIT] | "
bash ecmcReport.bash $REPORT "--- | --- |"

for TRIGGVAL in {5001..5010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV=$REF_PV
   REF_VAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL=$(echo $REF_VAL | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS+="$REF_VAL "
   echo "FWD switch engage position $TRIGGVAL: $REF_VAL"
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL >> $REPORT
   if (( $(echo "$REF_VAL > $REF_MAX" |bc -l) )); then
     REF_MAX=$REF_VAL
   fi
   if (( $(echo "$REF_VAL < $REF_MIN" |bc -l) )); then
     REF_MIN=$REF_VAL
   fi
done

# Calc avg and std
REF_AVG=$(echo "$REF_VALS" | bash ecmcAvgDataRow.bash)
REF_STD=$(echo "$REF_VALS" | bash ecmcStdDataRow.bash)
REF_RANGE=$(echo "$REF_MAX-($REF_MIN)" |bc -l)
echo "Reference AVG=$REF_AVG, STD=$REF_STD"
printf "AVG | %.${DEC}f |\n" $REF_AVG >> $REPORT
printf "STD | %.${DEC}f |\n" $REF_STD >> $REPORT
printf "Range | %.${DEC}f |\n" $REF_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""

# Disengage
SWITCHVAL=1
REF_VALS=""
REF_AVG=""
REF_STD=""
COUNTER=0
REF_MIN=10000;
REF_MAX=-10000;

bash ecmcReport.bash $REPORT "## High Limit Disengage Position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test |  Reference [$UNIT]|"
bash ecmcReport.bash $REPORT "--- | --- |"

for TRIGGVAL in {5011..5020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV=$REF_PV
   REF_VAL=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL=$(echo $REF_VAL | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS+="$REF_VAL "
   echo "FWD switch disengage position $TRIGGVAL: $REF_VAL"
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL >> $REPORT
   if (( $(echo "$REF_VAL > $REF_MAX" |bc -l) )); then
     REF_MAX=$REF_VAL
   fi
   if (( $(echo "$REF_VAL < $REF_MIN" |bc -l) )); then
     REF_MIN=$REF_VAL
   fi
done

# Calc avg and std
REF_AVG=$(echo "$REF_VALS" | bash ecmcAvgDataRow.bash)
REF_STD=$(echo "$REF_VALS" | bash ecmcStdDataRow.bash)
REF_RANGE=$(echo "$REF_MAX-($REF_MIN)" |bc -l)
echo "Reference AVG=$REF_AVG, STD=$REF_STD"
printf "AVG | %.${DEC}f |\n" $REF_AVG >> $REPORT
printf "STD | %.${DEC}f |\n" $REF_STD >> $REPORT
printf "Range | %.${DEC}f |\n" $REF_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""
