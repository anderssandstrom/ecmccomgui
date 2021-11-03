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
#  Script for extracting and calculating statistics of limit switch
#  engage/disengage performance.
#
#  Arguments:
#    1 Data file   (input)
#    2 Report file (output)
#    3 TEST_PV
#    4 REF_PV
#    5 REF gain
#    6 REF offset
#    7 LOW_LIM_PV 
#    8 HIGH_LIM_PV
#    9 Decimals
#    10 Unit
#
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

############ LOW LIMIT SWITCH
# Low limit
bash ecmcReport.bash $REPORT "# Limit Switch Performance"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT " ## Configuration"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Setting | Value |"
bash ecmcReport.bash $REPORT "--- | --- |"
bash ecmcReport.bash $REPORT "Data file | $FILE |"
bash ecmcReport.bash $REPORT "Reference position source  | $REF_PV |"
bash ecmcReport.bash $REPORT "Reference gear ratio  | $REF_GR |"
bash ecmcReport.bash $REPORT "Reference offset  | $REF_OFF |"
bash ecmcReport.bash $REPORT "Low Limit source  | $LOW_LIM_PV |"
bash ecmcReport.bash $REPORT "High Limit source  | $HIGH_LIM_PV |"
bash ecmcReport.bash $REPORT "Test number source  | $TEST_PV |"
bash ecmcReport.bash $REPORT "Unit  | $UNIT |"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "## Low Limit"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Engage [$UNIT] | Disengage [$UNIT] |"
bash ecmcReport.bash $REPORT "--- | --- | --- |"

# Get one reference value just before BI1 0
TRIGGPV=$TEST_PV
DATACOUNT="400"  # Must be enough to capture the switch transition
SWITCHPV=$LOW_LIM_PV
SWITCHVAL=0
REF_VALS=""
COUNTER=0

# this is uggly...
REF_MIN_1=10000;
REF_MAX_1=-10000;
# Engage
for TRIGGVAL in {3001..3010}
do
   let "COUNTER=$COUNTER+1"   
   DATAPV=$REF_PV
   REF_VAL_1=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL_1=$(echo $REF_VAL_1 | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS_1+="$REF_VAL_1 "
   echo "BWD switch engage position $TRIGGVAL: $REF_VAL_1"
   
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL_1 >> $REPORT

   if (( $(echo "$REF_VAL_1 > $REF_MAX_1" | bc -l) )); then
     REF_MAX_1=$REF_VAL_1
   fi
   if (( $(echo "$REF_VAL_1 < $REF_MIN_1" | bc -l) )); then
     REF_MIN_1=$REF_VAL_1
   fi

done

# Calc avg and std
REF_AVG_1=$(echo "$REF_VALS_1" | bash ecmcAvgDataRow.bash)
REF_STD_1=$(echo "$REF_VALS_1" | bash ecmcStdDataRow.bash)
REF_RANGE_1=$(echo "$REF_MAX_1-($REF_MIN_1)" | bc -l)
echo "Reference AVG=$REF_AVG, STD=$REF_STD_1"
#printf "AVG | %.${DEC}f | \n" $REF_AVG_1 >> $REPORT
#printf "STD | %.${DEC}f | \n" $REF_STD_1 >> $REPORT
#printf "Range | %.${DEC}f\n"  $REF_RANGE_1 >> $REPORT

echo "REF_MIN_1=$REF_MIN_1, REF_MAX_1=$REF_MAX_1, REF_RANGE_1=$REF_RANGE_1"

bash ecmcReport.bash $REPORT ""

# Disengage
#bash ecmcReport.bash $REPORT "## Low Limit Disengage Position "
#bash ecmcReport.bash $REPORT ""
#bash ecmcReport.bash $REPORT "Test | Reference [$UNIT] "
#bash ecmcReport.bash $REPORT "--- | --- |"

SWITCHVAL=1
REF_VALS=""
REF_AVG=""
COUNTER=0
REF_MIN_2=10000;
REF_MAX_2=-10000;

for TRIGGVAL in {3011..3020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV=$REF_PV
   REF_VAL_2=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL_2=$(echo $REF_VAL_2 | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS_2+="$REF_VAL_2 "
   echo "BWD switch disengage position $TRIGGVAL: $REF_VAL_2"
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL_2 >> $REPORT
   if (( $(echo "$REF_VAL_2 > $REF_MAX_2" |bc -l) )); then
     REF_MAX_2=$REF_VAL_2
   fi
   if (( $(echo "$REF_VAL_2 < $REF_MIN_2" |bc -l) )); then
     REF_MIN_2=$REF_VAL_2
   fi
done

# Calc avg and std
REF_AVG_2=$(echo "$REF_VALS_2" | bash ecmcAvgDataRow.bash)
REF_STD=_2$(echo "$REF_VALS_2" | bash ecmcStdDataRow.bash)
REF_RANGE_2=$(echo "$REF_MAX_2-($REF_MIN_2)" |bc -l)
echo "Reference AVG=$REF_AVG_2, STD=$REF_STD_2"
printf "AVG   | %.${DEC}f | %.${DEC}f |\n" $REF_AVG_1  $REF_AVG_2 >> $REPORT
printf "STD   | %.${DEC}f | %.${DEC}f |\n" $REF_STD_1  $REF_STD_2 >> $REPORT
printf "Range | %.${DEC}f | %.${DEC}f |\n" $REF_RANGE_1  $REF_RANGE_2 >> $REPORT
bash ecmcReport.bash $REPORT ""

############ HIGH LIMIT SWITCH
# Engage
SWITCHPV=$HIGH_LIM_PV
SWITCHVAL=0
REF_VALS=""
REF_AVG=""
COUNTER=0
REF_MIN_3=10000;
REF_MAX_3=-10000;

bash ecmcReport.bash $REPORT "## High Limit "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "Test | Engage [$UNIT] | Disengage [$UNIT] |"
bash ecmcReport.bash $REPORT "--- | --- | --- |"

for TRIGGVAL in {5001..5010}
do
   let "COUNTER=$COUNTER+1"
   DATAPV=$REF_PV
   REF_VAL_3=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL_3=$(echo $REF_VAL_3 | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS_3+="$REF_VAL_3 "
   echo "FWD switch engage position $TRIGGVAL: $REF_VAL_3"
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL_3_3 >> $REPORT
   if (( $(echo "$REF_VAL_3 > $REF_MAX_3" |bc -l) )); then
     REF_MAX_3=$REF_VAL_3
   fi
   if (( $(echo "$REF_VAL_3 < $REF_MIN_3" |bc -l) )); then
     REF_MIN_3=$REF_VAL_3
   fi
done

# Calc avg and std
REF_AVG=$(echo "$REF_VALS_3" | bash ecmcAvgDataRow.bash)
REF_STD=$(echo "$REF_VALS_3" | bash ecmcStdDataRow.bash)
REF_RANGE=$(echo "$REF_MAX_3-($REF_MIN_3)" |bc -l)
echo "Reference AVG=$REF_AVG_3, STD=$REF_STD_3"
#printf "AVG | %.${DEC}f |\n" $REF_AVG >> $REPORT
#printf "STD | %.${DEC}f |\n" $REF_STD >> $REPORT
#printf "Range | %.${DEC}f |\n" $REF_RANGE >> $REPORT
bash ecmcReport.bash $REPORT ""

# Disengage
SWITCHVAL=1
REF_VALS=""
REF_AVG=""
REF_STD=""
COUNTER=0
REF_MIN_4=10000;
REF_MAX_4=-10000;

#sbash ecmcReport.bash $REPORT "## High Limit Disengage Position "
#sbash ecmcReport.bash $REPORT ""
#sbash ecmcReport.bash $REPORT "Test |  Reference [$UNIT]|"
#sbash ecmcReport.bash $REPORT "--- | --- |"

for TRIGGVAL in {5011..5020}
do
   let "COUNTER=$COUNTER+1"
   DATAPV=$REF_PV
   REF_VAL_4=$(bash ecmcGetSwitchPosValue.bash $FILE $TRIGGPV $TRIGGVAL $DATAPV $DATACOUNT $SWITCHPV $SWITCHVAL)
   REF_VAL_4=$(echo $REF_VAL_4 | bash ecmcScaleOffsetData.bash ${REF_GR} ${REF_OFF})
   REF_VALS_4+="$REF_VAL_4 "
   echo "FWD switch disengage position $TRIGGVAL: $REF_VAL_4_4"
   printf "%d | %.${DEC}f |\n" $COUNTER $REF_VAL_4 >> $REPORT
   if (( $(echo "$REF_VAL_4 > $REF_MAX_4" |bc -l) )); then
     REF_MAX_4=$REF_VAL_4
   fi
   if (( $(echo "$REF_VAL_4 < $REF_MIN_4" |bc -l) )); then
     REF_MIN_4=$REF_VAL_4v
   fi
done

# Calc avg and std
REF_AVG_4=$(echo "$REF_VALS_4" | bash ecmcAvgDataRow.bash)
REF_STD_4=$(echo "$REF_VALS_4" | bash ecmcStdDataRow.bash)
REF_RANGE_4=$(echo "$REF_MAX_4-($REF_MIN_4)" |bc -l)
echo "Reference AVG=$REF_AVG_4, STD=$REF_STD_4"
printf "AVG   | %.${DEC}f | %.${DEC}f |\n" $REF_AVG_3  $REF_AVG_4 >> $REPORT
printf "STD   | %.${DEC}f | %.${DEC}f |\n" $REF_STD_3  $REF_STD_4 >> $REPORT
printf "Range | %.${DEC}f | %.${DEC}f |\n" $REF_RANGE_3  $REF_RANGE_4 >> $REPORT
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT ""
