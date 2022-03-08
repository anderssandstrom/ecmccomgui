#!/bin/bash
# 
# Main script for processing data for bifrost slitset SAT.
#
# Arg 1 Data file   (input)
# Arg 2 Report file (output)
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#
# Data examples: 
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
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.629165 1.602243125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.679157 66.06747913  
# IOC_TEST:m0s005-Enc01-PosAct   2021-10-27 09:04:48.679157 33.08044  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.679157 1.639765625  
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.679157 1.639743125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.729143 66.01678658  
# IOC_TEST:m0s005-Enc01-PosAct   2021-10-27 09:04:48.729143 2147.483643  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.729143 1.677265625  
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.729143 1.677243125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.779143 65.96195507  
# IOC_TEST:m0s005-Enc01-PosAct   2021-10-27 09:04:48.779143 33.35992  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.779143 1.714765625  
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.779143 1.714743125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.829164 65.91618061  
# IOC_TEST:m0s005-Enc01-PosAct   2021-10-27 09:04:48.829164 2147.483643  
# IOC_TEST:Axis1-PosAct          2021-10-27 09:04:48.829164 1.752265625  
# IOC_TEST:Axis1-PosSet          2021-10-27 09:04:48.829164 1.752243125  
# IOC_TEST:m0s004-Enc01-PosAct   2021-10-27 09:04:48.879143 65.88419342  
#
# Markdown to PDF notes
# 1: https://www.markdowntopdf.com
# 2: 
# pip install grip  
# grip your_markdown.md
# grip will render the markdown on localhost:5000 or similar (ex: go to http://localhost:5000/) - just edit away and refresh the browser. Print when ready.




# Newline
nl='
'
if [ "$#" -ne 2 ]; then
   echo "main: Wrong arg count... Please specify input and output file."
   exit 1 
fi

### Need to update these fileds for every FAT sat so everything is correct
##PV names:
MOTORACTPV="IOC_TEST:Axis1-PosAct"
MOTORSETPV="IOC_TEST:Axis1-PosSet"
RESOLVERPV="IOC_TEST:m0s004-Enc01-PosAct"
REFERENCEPV="IOC_TEST:m0s005-Enc01-PosAct"
TESTNUMPV="IOC_TEST:TestNumber"

# Number decimals
DEC=5
UNIT="mm"
# Calculate gearratios based on this test
#TESTNUM_GEARRATIO_FROM=1501
#TESTNUM_GEARRATIO_TO=1502

TESTNUM_GEARRATIO_FROM=1501
TESTNUM_GEARRATIO_TO=2501

# this many sample before this test (needs to be bigger than samples between TESTNUM_GEARRATIO_FROM to TESTNUM_GEARRATIO_TO)
SAMPLES_GEARRATIO=1000000

# Defs for ISO230 analysis
ISO230_POS_COUNT=5
ISO230_CYCLE_COUNT=5

FILE=$1
REPORT=$2

echo "Collect gear ratio data (only at test points in the matrix)...."
GEAR_RATIO_DATA=$(bash mainCollectDataForGearRatioCalc.bash $FILE $ISO230_CYCLE_COUNT $ISO230_POS_COUNT)

## Init report file
bash ecmcReportInit.bash $REPORT $FILE

# Use gear ratio python script to find gear ratios
echo "1. Calculate gear ratios..."

#### Use these lines if gear rations should be based on all data colelcted in iso230 cycle
# Filter data for gear ratio calculations
#GEAR_RATIO_DATA=$(cat $FILE | grep -A$SAMPLES_GEARRATIO " $TESTNUM_GEARRATIO_FROM" | grep -B$SAMPLES_GEARRATIO " $TESTNUM_GEARRATIO_TO" )
# Filter outlieres of Micro epsilon sensor (values above 2000 is excluded)
#GEAR_RATIO_DATA=$(echo "$GEAR_RATIO_DATA " |  awk ' {if ($4<2000) print;}')

# Resolver to open loop use test 1503
TEMP=$(echo "$GEAR_RATIO_DATA " | grep -E "$MOTORACTPV|$RESOLVERPV|$TESTNUMPV" | grep -B $SAMPLES_GEARRATIO " $TESTNUM_GEARRATIO" |  python ../pyDataManip/ecmcGearRatioIgnoreTimeStamps.py "$MOTORACTPV" "$RESOLVERPV")

echo "$TEMP"
# Gear ratio resolver
RES_GR=$(echo $TEMP | awk '{print $1}')
RES_OFF=$(echo $TEMP | awk '{print $2}')
RES_LEN=$(echo $TEMP | awk '{print $3}')
RES_ERR=$(echo $TEMP | awk '{print $4}')
echo "RES GR=$RES_GR, OFF=$RES_OFF, LEN=$RES_LEN, RESIDUAL=$RES_ERR"

# Reference to open loop use test 1503 filter values above  2000 #awk '{if($4<2000){ print}}'| 
TEMP=$(echo "$GEAR_RATIO_DATA " | grep -E "$MOTORACTPV|$REFERENCEPV|$TESTNUMPV" | grep -B $SAMPLES_GEARRATIO " $TESTNUM_GEARRATIO" |  python ../pyDataManip/ecmcGearRatioIgnoreTimeStamps.py "$MOTORACTPV" "$REFERENCEPV")
echo "$TEMP"
# Gear ratio reference
REF_GR=$(echo $TEMP | awk '{print $1}')
REF_OFF=$(echo $TEMP | awk '{print $2}')
REF_LEN=$(echo $TEMP | awk '{print $3}')
REF_ERR=$(echo $TEMP | awk '{print $4}')
echo "REF GR=$REF_GR, OFF=$REF_OFF, LEN=$REF_LEN, RESIDUAL=$REF_ERR"

echo "2. ISO230-2 test..."

# Always 5 cycles in standard
# Get forward direction data points (test numbers 1xx1..1xx)
TESTS=$(seq -w 1 1 $ISO230_POS_COUNT)
CYCLES=$(seq -w 1 1 $ISO230_CYCLE_COUNT)

RES_ERR_DISP=$(echo "scale=$DEC;$RES_ERR/1" | bc -l)
RES_LEN_DISP=$(echo "scale=$DEC;$RES_LEN/1" | bc -l)
RES_GR_DISP=$(echo "scale=$DEC;$RES_GR/1" | bc -l)
RES_OFF_DISP=$(echo "scale=$DEC;$RES_OFF/1" | bc -l)


REF_ERR_DISP=$(echo "scale=$DEC;$REF_ERR/1" | bc -l)
REF_LEN_DISP=$(echo "scale=$DEC;$REF_LEN/1" | bc -l)
REF_GR_DISP=$(echo "scale=$DEC;$REF_GR/1" | bc -l)
REF_OFF_DISP=$(echo "scale=$DEC;$REF_OFF/1" | bc -l)

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Gear Ratios"
bash ecmcReport.bash $REPORT "From | To | Ratio [] | Offset [$UNIT] | Data count [] | Residual error [$UNIT²]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- | --- | --- |"
bash ecmcReport.bash $REPORT "Openloop | Resolver | $RES_GR_DISP | $RES_OFF_DISP | $RES_LEN_DISP | $RES_ERR_DISP "
bash ecmcReport.bash $REPORT "Openloop | Reference (ILD2300) | $REF_GR_DISP | $REF_OFF_DISP | $REF_LEN_DISP | $REF_ERR_DISP "
bash ecmcReport.bash $REPORT ""

# Forward tests
bash ecmcReport.bash $REPORT "# Forward test sequence"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "i (pos id)| j (cycle)| Tgt_pos(i,j) [$UNIT] | Motor(i,j) [$UNIT] | Resolver(i,j) [$UNIT] | Reference(i,j) [$UNIT] | x(i,j) (diff ref-tgt),  [$UNIT]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- | --- | --- |--- |"
TESTNUMBER_BASE=1
DIFF_SUM=0
TEST_COUNTER=0
for TEST in $TESTS
do   
  eval "DIFF_FWD_SUM_AT_POS_$TEST=0"
done

for CYCLE in $CYCLES;
do
  echo "CYCLE=$CYCLE"

  for TEST in $TESTS
  do   
   TESTNUMBER=$TESTNUMBER_BASE$CYCLE"0"$TEST
   echo "TESTNUMBER=$TESTNUMBER"

   # Target position
   DATAPV=$MOTORSETPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   TGT_DATA=$DATA
   echo "TGT_DATA=$DATA" 
   eval "TGT_FWD_$CYCLE$TEST=$DATA"
   eval "TGT_POS_$TEST=$TGT_DATA"

   
   # Open loop counter
   DATAPV=$MOTORACTPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   OL_DATA=$DATA
   echo "OL_DATA=$DATA" 
   eval "OL_FWD_$CYCLE$TEST=$DATA"

   # Resolver
   DATAPV=$RESOLVERPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(bc -l <<< "$DATA*($RES_GR)+($RES_OFF)")
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   RES_DATA=$DATA
   echo "RES_DATA=$DATA" 
   eval "RES_FWD_$CYCLE$TEST=$DATA"

   # Reference
   DATAPV=$REFERENCEPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(bc -l <<< "$DATA*($REF_GR)+($REF_OFF)")
   DATA=$(echo "scale=$DEC;$DATA/1" | bc )
   REF_DATA=$DATA
   echo "REF_DATA=$DATA"   
   eval "REF_FWD_$CYCLE$TEST=$DATA"
   
   # Calc diff ref tg Xij
   DIFF=$(echo "scale=$DEC;$REF_DATA-$TGT_DATA" | bc -l)
   eval "X_FWD_$TEST_$CYCLE=$DIFF"
   DIFF_SUM=$(echo "$DIFF_SUM+($DIFF)" | bc -l) 

   # Sum error at this position
   TEMP_VAR="DIFF_FWD_SUM_AT_POS_$TEST"
   TEMP=${!TEMP_VAR}
   TEMP=$(echo "$TEMP+($DIFF)" | bc -l)
   eval "$TEMP_VAR=$TEMP"
   
   bash ecmcReport.bash $REPORT " $TEST | $CYCLE | $TGT_DATA | $OL_DATA | $RES_DATA | $REF_DATA | $DIFF |"
   let TEST_COUNTER=TEST_COUNTER+1
  done
done
bash ecmcReport.bash $REPORT ""


#Mean unidirectional pos dev at a position
DIFF_AVG_FWD=$(echo "$DIFF_SUM/$TEST_COUNTER" | bc -l) 

# Backward tests
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Backward test sequence"
bash ecmcReport.bash $REPORT "i (pos id)| j (cycle)| Tgt_pos(i,j) [$UNIT] | Motor(i,j) [$UNIT] | Resolver(i,j) [$UNIT] | Reference(i,j) [$UNIT] | x(i,j) (diff ref-tgt),  [$UNIT]"
bash ecmcReport.bash $REPORT "--- | --- | --- | --- | --- | --- |--- |"

TESTNUMBER_BASE=2
DIFF_SUM=0
TEST_COUNTER=0
for TEST in $TESTS
do   
  eval "DIFF_BWD_SUM_AT_POS_$TEST=0"
done


for CYCLE in $CYCLES;
do
  echo "CYCLE=$CYCLE"

  for TEST in $TESTS
  do   
   TESTNUMBER=$TESTNUMBER_BASE$CYCLE"0"$TEST
   echo "TESTNUMBER=$TESTNUMBER"
   
   # Target position
   DATAPV=$MOTORSETPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   TGT_DATA=$DATA
   echo "TGT_DATA=$DATA" 
   eval "TGT_BWD_$CYCLE$TEST=$DATA"
   eval "TGT_POS_$TEST=$TGT_DATA"

   # Open loop counter
   DATAPV=$MOTORACTPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT}) 
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   OL_DATA=$DATA
   echo "OL_DATA=$DATA" 
   eval "OL_BWD_$CYCLE$TEST=$DATA"

   # Resolver
   DATAPV=$RESOLVERPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(bc -l <<< "$DATA*($RES_GR)+($RES_OFF)")
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   RES_DATA=$DATA
   echo "RES_DATA=$DATA" 
   eval "RES_BWD_$CYCLE$TEST=$DATA"

   # Reference
   DATAPV=$REFERENCEPV
   TRIGGPV=$TESTNUMPV
   TRIGGVAL=$TESTNUMBER
   DATACOUNT=1
   DATA=$(bash ecmcGetDataBeforeTrigg.bash ${FILE} ${TRIGGPV} ${TRIGGVAL} ${DATAPV} ${DATACOUNT})   
   DATA=$(bc -l <<< "$DATA*($REF_GR)+($REF_OFF)")
   DATA=$(echo "scale=$DEC;$DATA/1" | bc -l)
   REF_DATA=$DATA
   echo "REF_DATA=$DATA"   
   eval "REF_BWD_$CYCLE$TEST=$DATA"


   # Sum error at this position
   TEMP_VAR="DIFF_FWD_SUM_AT_POS_$TEST"
   TEMP=${!TEMP_VAR}
   TEMP=$(echo "$TEMP+($DIFF)" | bc -l)
   eval "$TEMP_VAR=$TEMP"


   # Calc diff ref tg Xij
   DIFF=$(echo "scale=$DEC;$REF_DATA-($TGT_DATA)" | bc -l)
   eval "X_BWD_$TEST_$CYCLE=$DIFF"
   DIFF_SUM=$(echo "$DIFF_SUM+($DIFF)" | bc -l) 
   
   # Sum error at this position
   TEMP_VAR="DIFF_BWD_SUM_AT_POS_$TEST"
   TEMP=${!TEMP_VAR}
   TEMP=$(echo "$TEMP+($DIFF)" | bc )
   eval "$TEMP_VAR=$TEMP"

   bash ecmcReport.bash $REPORT " $TEST | $CYCLE | $TGT_DATA | $OL_DATA | $RES_DATA | $REF_DATA | $DIFF |"
   let TEST_COUNTER=TEST_COUNTER+1
  done
done
bash ecmcReport.bash $REPORT ""

# Mean unidirectional pos dev at a position
DIFF_AVG_BWD=$(echo "$DIFF_SUM/$TEST_COUNTER" | bc) 

# Calc x_dash_i (Mean unidirectional pos deviation at position i)
B_MAX=0
B_SUM=0
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Mean Position Deviation and Reversal Error"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "X_fwd(i) = Mean unidirectional positioning deviation at a position (fwd dir)"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "X_bwd(i) = Mean unidirectional positioning deviation at a position (bwd dir)"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "X_avg(i) = Mean bi-directional positioning deviation at a position"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "B(i) = Reversal error at a position "
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "i (pos id) | Tgt_pos(i) [$UNIT] | X_fwd(i) [$UNIT] | X_bwd(i) [$UNIT] | X_avg(i) [$UNIT] | B(i) [$UNIT]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |--- |--- |"
for TEST in $TESTS
do
  TGT_VAR_NAME="TGT_POS_$TEST"
  TGT=${!TGT_VAR_NAME}
  # Forward
  TEMP_VAR_NAME="DIFF_FWD_SUM_AT_POS_$TEST"
  TEMP_FWD=${!TEMP_VAR_NAME}
  TEMP_FWD=$(echo "scale=$DEC;$TEMP_FWD/$ISO230_POS_COUNT" | bc -l)
  eval "X_FWD_AVG_$TEST=$TEMP_FWD"  

  # Backward
  TEMP_VAR_NAME="DIFF_BWD_SUM_AT_POS_$TEST"
  TEMP_BWD=${!TEMP_VAR_NAME}
  TEMP_BWD=$(echo "scale=$DEC;$TEMP_BWD/$ISO230_POS_COUNT" | bc -l)
  eval "X_BWD_AVG_$TEST=$TEMP_BWD"  

  TEMP_AVG=$(echo "scale=$DEC;($TEMP_BWD+$TEMP_FWD)/2" | bc -l)
  eval "X_AVG_$TEST=$TEMP_AVG"

  B_i=$(echo "scale=$DEC;($TEMP_FWD)-($TEMP_BWD)" | bc -l)
  eval "B_$TEST=$B_i"
  bash ecmcReport.bash $REPORT " $TEST | $TGT | $TEMP_FWD | $TEMP_BWD | $TEMP_AVG | $B_i"
  # abs value ${var#-} (remove -)
  if (( $(echo "${B_i#-} > $B_MAX" |bc -l) )); then
    B_MAX=${B_i#-}
  fi
  B_SUM=$(echo "$B_SUM+($B_i)" | bc -l)  
done
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "B = Axis Reversal Error"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "B = $B_MAX [$UNIT]"
bash ecmcReport.bash $REPORT ""
B_AVG=$(echo "scale=$DEC;$B_SUM/($ISO230_POS_COUNT)" | bc -l)  
bash ecmcReport.bash $REPORT "B_avg = Axis Avg. Reversal Error."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "B_avg = $B_AVG [$UNIT]"

########## REPEATABILITY
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Repeatability "
bash ecmcReport.bash $REPORT ""

# j=cycle 1..n  sqrt(1/(n-1)* E (xij-xi_avg)²)
# calc sum of (xij-xi_avg)²
# 
#xi=X_FWD_$TEST_$CYCLE
#xi_avg=X_FWD_AVG_$TEST

bash ecmcReport.bash $REPORT "S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R_fwd(i) = Forward unidirectional positioning repeatability at a position."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R_bwd(i) = Backward unidirectional positioning repeatability at a position."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R(i) = Bi-directional position repeatability at a position."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "i (pos id) | Tgt_pos(i) [$UNIT] | S_fwd(i) [$UNIT] | S_bwd(i) [$UNIT] | R_fwd(i) [$UNIT] | R_bwd(i) [$UNIT] | R(i) [$UNIT]"
bash ecmcReport.bash $REPORT "--- | --- | --- |--- |--- |--- |--- |"
R_FWD_MAX=0
R_BWD_MAX=0

for TEST in $TESTS
do
  TGT_VAR_NAME="TGT_POS_$TEST"
  TGT=${!TGT_VAR_NAME}
  STEMPSUM_FWD=0
  STEMPSUM_BWD=0
  for CYCLE in $CYCLES;
  do
    # FORWARD
    XIJ_VAR="X_FWD_$TEST_$CYCLE"
    XI_AVG_VAR="X_FWD_AVG_$TEST"
    XIJ=${!XIJ_VAR}
    XI_AVG=${!XI_AVG_VAR}
    STEMP=$(echo "($XIJ)-($XI_AVG)" | bc -l)
    STEMP2=$(echo "($STEMP)*($STEMP)" | bc -l)
    STEMPSUM_FWD=$(echo "($STEMPSUM_FWD)+($STEMP2)" | bc -l)

    # BACKWARD
    XIJ_VAR="X_BWD_$TEST_$CYCLE"
    XI_AVG_VAR="X_BWD_AVG_$TEST"
    XIJ=${!XIJ_VAR}
    XI_AVG=${!XI_AVG_VAR}
    STEMP=$(echo "($XIJ)-($XI_AVG)" | bc -l)
    STEMP2=$(echo "($STEMP)*($STEMP)" | bc -l)
    STEMPSUM_BWD=$(echo "($STEMPSUM_BWD)+($STEMP2)" | bc -l)
  done
  # * 1/(1-n)
  echo "HEHEHEHEHEH: STEMPSUM_FWD=$STEMPSUM_FWD"
  STEMP_FWD=$(echo "scale=$DEC;sqrt(($STEMPSUM_FWD)/4)" | bc -l)
  eval "S_FWD_$TEST=$STEMP_FWD"
  echo "S_FWD_$TEST=$STEMP_FWD, $STEMPSUM_FWD"
  echo "HEHEHEHEHEH: STEMPSUM_BWD=$STEMPSUM_BWD"
  STEMP_BWD=$(echo "scale=$DEC;sqrt(($STEMPSUM_BWD)/4)" | bc -l)
  eval "S_BWD_$TEST=$STEMP_BWD"
  echo "S_BWD_$TEST=$STEMP_BWD, $STEMPSUM_BWD"
  #Ri=4*Si
  RTEMP_FWD=$(echo "scale=$DEC;4*$STEMP_FWD" | bc -l)  
  eval "R_FWD_$TEST=$RTEMP_FWD"
  RTEMP_BWD=$(echo "scale=$DEC;4*$STEMP_BWD" | bc -l)
  eval "R_BWD_$TEST=$RTEMP_BWD"
  
  #Rmaxfwd
  if (( $(echo "$RTEMP_FWD > $R_FWD_MAX" | bc -l) )); then
    R_FWD_MAX=$RTEMP_FWD
  fi
  #Rmaxbwd
  if (( $(echo "$RTEMP_BWD > $R_BWD_MAX" | bc -l) )); then
    R_BWD_MAX=$RTEMP_BWD
  fi
  
  
  # Calc bi-directional positioning repeatability at a position Ri
  BIVAR="B_$TEST"
  BI=${!BIVAR}

  RTEMP_1=$(echo "2*($STEMP_FWD)+2*($STEMP_BWD)+sqrt(($BI)*($BI))" | bc -l)
  RTEMP_2=$STEMP_FWD;
  RTEMP_3=$STEMP_BWD;
  RI=$RTEMP_1
  # R_i is max of RTEMP_1..3
  if (( $(echo "$RTEMP_2 > $RI" | bc -l) )); then
    RI=$RTEMP_2
  fi
  if (( $(echo "$RTEMP_3 > $RI" | bc -l) )); then
    RI=$RTEMP_3
  fi
  RI=$(echo "scale=$DEC;$RI/1" | bc -l)
  eval "R_I_$TEST=$RI"
  bash ecmcReport.bash $REPORT " $TEST| $TGT | $STEMP_FWD |$STEMP_BWD | $RTEMP_FWD | $RTEMP_BWD | $RI"

done
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i)))"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R_fwd = $R_FWD_MAX [$UNIT]"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i)))"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R_bwd = $R_BWD_MAX [$UNIT]"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd))"
R=$R_FWD_MAX
if (( $(echo "$R_BWD_MAX > $R" | bc -l) )); then
  R=$R_BWD_MAX
fi
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "R = $R [$UNIT]"
bash ecmcReport.bash $REPORT ""

########## Systematic positioning error
# E_fwd = max(x_fwd_avg(i))-min(x_fwd_avg(i))

# Init with forst value
XI_FWD_AVG_MAX=$X_FWD_AVG_1
XI_BWD_AVG_MAX=$X_BWD_AVG_1
XI_FWD_AVG_MIN=$X_FWD_AVG_1
XI_BWD_AVG_MIN=$X_BWD_AVG_1
XI_MAX=$X_AVG_1
XI_MIN=$X_AVG_1
for TEST in $TESTS
do
    # FORWARD
    XI_AVG_VAR="X_FWD_AVG_$TEST"
    XI_AVG=${!XI_AVG_VAR}
    # Check max
    if (( $(echo "$XI_AVG > $XI_FWD_AVG_MAX" | bc -l) )); then
      XI_FWD_AVG_MAX=$XI_AVG
    fi
    # Check min
    if (( $(echo "$XI_AVG < $XI_FWD_AVG_MIN" | bc -l) )); then
      XI_FWD_AVG_MIN=$XI_AVG
    fi

    # BACKWARD
    XI_AVG_VAR="X_BWD_AVG_$TEST"    
    XI_AVG=${!XI_AVG_VAR}
    # Check max
    if (( $(echo "$XI_AVG > $XI_BWD_AVG_MAX" | bc -l) )); then
      XI_BWD_AVG_MAX=$XI_AVG
    fi
    # Check min
    if (( $(echo "$XI_AVG < $XI_BWD_AVG_MIN" | bc -l) )); then
      XI_BWD_AVG_MIN=$XI_AVG
    fi
        
    # Bi dir
    XI_AVG_VAR="X_AVG_$TEST"    
    XI_AVG=${!XI_AVG_VAR}
    # Check max
    if (( $(echo "$XI_AVG > $XI_MAX" | bc -l) )); then
      XI_MAX=$XI_AVG
    fi
    # Check min
    if (( $(echo "$XI_AVG < $XI_MIN" | bc -l) )); then
      XI_MIN=$XI_AVG
    fi

done

E_fwd=$(echo "scale=$DEC;$XI_FWD_AVG_MAX-($XI_FWD_AVG_MIN)" | bc -l)
E_bwd=$(echo "scale=$DEC;$XI_BWD_AVG_MAX-($XI_BWD_AVG_MIN)" | bc -l)

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Positioning Error "

bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "E_fwd = Forward unidirectional system positioning error of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "E_fwd = $E_fwd [$UNIT]"
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "E_bwd = Backward unidirectional system positioning error of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "E_bwd = $E_bwd [$UNIT]"
bash ecmcReport.bash $REPORT ""

# Check max of fwd bwd
XI_AVG_MAX=$XI_FWD_AVG_MAX
if (( $(echo "$XI_BWD_AVG_MAX > $XI_AVG_MAX" | bc -l) )); then
  XI_AVG_MAX=$XI_BWD_AVG_MAX
fi

# Check min of fwd bwd
XI_AVG_MIN=$XI_FWD_AVG_MIN
if (( $(echo "$XI_BWD_AVG_MIN < $XI_AVG_MIN" | bc -l) )); then
  XI_AVG_MIN=$XI_BWD_AVG_MIN
fi

E=$(echo "scale=$DEC;$XI_AVG_MAX-($XI_AVG_MIN)" | bc -l)
bash ecmcReport.bash $REPORT "E = Bi-directional system positioning error of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "E = $E [$UNIT]"
bash ecmcReport.bash $REPORT ""

# M=max(x_avg)-min(x_avg)
M=$(echo "scale=$DEC;$XI_MAX-($XI_MIN)" | bc -l)
bash ecmcReport.bash $REPORT "M = Mean bi-directional system positioning error of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "M = $M [$UNIT]"
bash ecmcReport.bash $REPORT ""


########## Accuracy

#A_fwd=max(Xi_avg_fwd+2*Si_fwd)-min(Xi_avg_fwd-2*Si_fwd)


echo "0 X_FWD_AVG_1=$X_FWD_AVG_1" 
echo "0 S_FWD_1=$S_FWD_1" 
echo "0 X_BWD_AVG_1=$X_BWD_AVG_1" 
echo "0 S_BWD_1=$S_BWD_1" 


XI_2SI_MAX_FWD=$(echo "$X_FWD_AVG_1+2*($S_FWD_1)" | bc -l)
XI_2SI_MIN_FWD=$(echo "$X_FWD_AVG_1-2*($S_FWD_1)" | bc -l)
XI_2SI_MAX_BWD=$(echo "$X_BWD_AVG_1+2*($S_BWD_1)" | bc -l)
XI_2SI_MIN_BWD=$(echo "$X_BWD_AVG_1-2*($S_BWD_1)" | bc -l)

echo "1 XI_2SI_MAX_FWD=$XI_2SI_MAX_FWD" 
echo "1 XI_2SI_MIN_FWD=$XI_2SI_MAX_FWD" 
echo "1 XI_2SI_MAX_BWD=$XI_2SI_MAX_FWD" 
echo "1 XI_2SI_MIN_BWD=$XI_2SI_MAX_FWD" 

for TEST in $TESTS
do
    echo "TEST=$TEST"
    # Calc Xi_avg_fwd+2*Si_fwd
    # FORWARD
    XI_AVG_VAR="X_FWD_AVG_$TEST"
    XI_AVG=${!XI_AVG_VAR}
    SI_VAR="S_FWD_$TEST"
    SI=${!SI_VAR}
    echo "XI_AVG=$XI_AVG"
    echo "SI=$SI"
    XI_PLUS_2SI=$(echo "$XI_AVG+2*($SI)" | bc -l)
    XI_MINUS_2SI=$(echo "$XI_AVG-2*($SI)" | bc -l)

    # Check max
    if (( $(echo "$XI_PLUS_2SI > $XI_2SI_MAX_FWD" | bc -l) )); then
      XI_2SI_MAX_FWD=$XI_PLUS_2SI
    fi
    # Check min
    if (( $(echo "$XI_MINUS_2SI < $XI_2SI_MIN_FWD" | bc -l) )); then
      XI_2SI_MIN_FWD=$XI_MINUS_2SI
    fi 

    echo "2 XI_2SI_MAX_FWD=$XI_2SI_MAX_FWD" 
    echo "2 XI_2SI_MIN_FWD=$XI_2SI_MIN_FWD" 

    # FORWARD
    XI_AVG_VAR="X_BWD_AVG_$TEST"
    XI_AVG=${!XI_AVG_VAR}
    SI_VAR="S_BWD_$TEST"
    SI=${!SI_VAR}
    echo "XI_AVG=$XI_AVG"
    echo "SI=$SI"
    XI_PLUS_2SI=$(echo "$XI_AVG+2*($SI)" | bc -l)
    XI_MINUS_2SI=$(echo "$XI_AVG-2*($SI)" | bc -l)
    # Check max
    if (( $(echo "$XI_PLUS_2SI > $XI_2SI_MAX_BWD" | bc -l) )); then
      XI_2SI_MAX_BWD=$XI_PLUS_2SI
    fi
    # Check min
    if (( $(echo "$XI_MINUS_2SI < $XI_2SI_MIN_BWD" | bc -l) )); then
      XI_2SI_MIN_BWD=$XI_MINUS_2SI
    fi 
    echo "2 XI_2SI_MAX_BWD=$XI_2SI_MAX_FWD" 
    echo "2 XI_2SI_MIN_BWD=$XI_2SI_MIN_FWD" 

done




bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "# Accuracy"
# A_fwd=XI_2SI_MAX_FWD-XI_2SI_MIN_FWD
bash ecmcReport.bash $REPORT ""
A_fwd=$(echo "scale=$DEC;$XI_2SI_MAX_FWD-($XI_2SI_MIN_FWD)" | bc -l)
bash ecmcReport.bash $REPORT "A_fwd = Forward unidirectional accuracy of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "A_fwd = $A_fwd [$UNIT]"
bash ecmcReport.bash $REPORT ""

A_bwd=$(echo "scale=$DEC;$XI_2SI_MAX_BWD-($XI_2SI_MIN_BWD)" | bc -l)
bash ecmcReport.bash $REPORT "A_bwd = Backward unidirectional accuracy of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "A_bwd = $A_bwd [$UNIT]"
bash ecmcReport.bash $REPORT ""

XI_2SI_MAX=$XI_2SI_MAX_FWD
# Check max
if (( $(echo "$XI_2SI_MAX_BWD > $XI_2SI_MAX" | bc -l) )); then
  XI_2SI_MAX=$XI_PLUS_2SI
fi

XI_2SI_MIN=$XI_2SI_MIN_FWD
# Check min
if (( $(echo "$XI_2SI_MIN_BWD < $XI_2SI_MIN" | bc -l) )); then
  XI_2SI_MIN=$XI_PLUS_2SI
fi

A=$(echo "scale=$DEC;$XI_2SI_MAX-($XI_2SI_MIN)" | bc -l)
bash ecmcReport.bash $REPORT "A = Bi-directional accuracy of an axis."
bash ecmcReport.bash $REPORT ""
bash ecmcReport.bash $REPORT "A = $A [$UNIT]"
bash ecmcReport.bash $REPORT ""



echo "####################################################################"

##### Switches ##########################################################
bash mainSwitchISO230.bash $FILE $REPORT $RES_GR $RES_OFF $REF_GR $REF_OFF $DEC

##### Resolver jitter ###################################################
bash mainResolverStandstillISO230.bash $FILE $REPORT $RES_GR $RES_OFF $REF_GR $REF_OFF 5 4000
