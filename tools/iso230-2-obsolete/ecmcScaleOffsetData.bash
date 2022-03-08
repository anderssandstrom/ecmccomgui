#!/bin/bash
# 
# Scale and offset data (first scale then offset)
#
# Arg 1 Optional file name, otherwise stdin
# Arg 2 Scale value
# Arg 3 Offset value
#
# Return Complete camonitor lines scaled (with PV name and timestamp).
#
# Example:Scale and offset all data from stdin with 10, 100
# bash ecmcScaleOffsetData.bash 10 100
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
  echo "ecmcScaleOffsetData: Wrong arg count..."
  exit 1  
fi

DATA=$(cat ${FILE} | awk -v CONVFMT=%.17g -v scale=${SCALE} -v offset=${OFFSET} '{$1*=scale;$1+=offset; print $0}')
echo "${DATA}"
