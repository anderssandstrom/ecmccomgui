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
   echo "mainRepeatability: Wrong arg count... Please specify input and output file."
   exit 1 
fi

FILE=$1
REPORT=$2
RESOLVER_OFFSET=$3
OPTO_OFFSET=$4
DEC=$5

bash ecmcReport.bash $REPORT "# Repeatability"

############## Pos 15 POS
bash mainRepeatabilitySubtest.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC 3100 3200
############## Pos 35 POS
bash mainRepeatabilitySubtest.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC 3300 3400
############## Pos 55 POS
bash mainRepeatabilitySubtest.bash $FILE $REPORT $RESOLVER_OFFSET $OPTO_OFFSET $DEC 3500 3600
