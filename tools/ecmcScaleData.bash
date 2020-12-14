#!/bin/bash
# 
# Scale data
#
# Arg 1 Optional file name, otherwise stdin
# Arg 2 Scale value
#
# Return List of scaled data only (without PV name and timestamp).
#
# Example:Scale all lines from stdin with 10
# bash ecmcScaleData.bash 10 
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

ARGOK=0
if [ "$#" -eq 1 ]; then
    FILE="-"
    SCALE=$1
    ARGOK=1
fi
if [ "$#" -eq 2 ]; then
    FILE=$1
    SCLAE=$2
    ARGOK=1
fi

if [ "$ARGOK" -ne 1 ]; then
  echo "ecmcScaleData: Wrong arg count..."
  exit 1  
fi

DATA=$(cat ${FILE} | awk -v CONVFMT=%.17g -v scale=${SCLAE} '{$1*=scale; print $0}')
echo "${DATA}"
