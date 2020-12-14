#!/bin/bash
# 
# Scale data in a camonitor text line
#
# Arg 1 Optional file name, otherwise stdin
# Arg 2 Scale value
#
# Return Complete camonitor lines scaled (with PV name and timestamp).
#
# Example:Scale all lines from stdin with 10
# bash ecmcScaleLines.bash 10 
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
    SCALE=$2
    ARGOK=1
fi

if [ "$ARGOK" -ne 1 ]; then
  echo "ecmcScaleLines: Wrong arg count..."
  exit 1  
fi

DATA=$(cat ${FILE} | awk -v CONVFMT=%.17g -v scale=${SCALE} '{$NF*=scale; print $0}')
echo "${DATA}"
