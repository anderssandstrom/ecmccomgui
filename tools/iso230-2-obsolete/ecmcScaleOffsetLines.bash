#!/bin/bash
# 
# Scale and offset data in a camonitor text line (scale first then offset)
#
# Arg 1 Optional file name, otherwise stdin
# Arg 2 Scale value
# Arg 3 Offset value
#
# Return Complete camonitor lines scaled (with PV name and timestamp).
#
# Example:Scale all lines from stdin with 10
# bash ecmcScaleLines.bash 10 
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

ARGOK=0
if [ "$#" -eq 2 ]; then
    FILE="-"
    SCALE=$1
    OFFSET=$2
    ARGOK=1
fi
if [ "$#" -eq 3 ]; then
    FILE=$1
    SCALE=$2
    OFFSET=$3
    ARGOK=1
fi

if [ "$ARGOK" -ne 1 ]; then
  echo "ecmcScaleOffsetLines: Wrong arg count..."
  exit 1  
fi

DATA=$(cat ${FILE} | awk -v CONVFMT=%.17g -v scale=${SCALE} -v offset=${OFFSET} '{$NF*=scale;$NF+=offset; print $0}')
echo "${DATA}"
