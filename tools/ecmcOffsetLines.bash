#!/bin/bash
# 
# Offset data in a camonitor text line
#
# Arg 1 Optional file name, otherwise stdin
# Arg 2 Offset value
#
# Return Complete camonitor lines offset (with PV name and timestamp).
#
# Example:Offset all lines from stdin with 10
# bash ecmcOffestLines.bash 10 
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

ARGOK=0
if [ "$#" -eq 1 ]; then
    FILE="-"
    OFFSET=$1
    ARGOK=1
fi
if [ "$#" -eq 2 ]; then
    FILE=$1
    OFFSET=$2
    ARGOK=1
fi

if [ "$ARGOK" -ne 1 ]; then
  echo "ecmcOffsetLines: Wrong arg count..."
  exit 1  
fi

DATA=$(cat ${FILE} | awk -v CONVFMT=%.17g -v offset=${OFFSET} '{$NF+=offset; print $0}')
echo "${DATA}"
