#!/bin/bash
# 
# Calc standard dev of elements in a list of camonitor rows
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Stdev value
#
# Example: Std all data in a row
# bash ecmcStdLines.bash
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

FILE="-"
if [ "$#" -eq 1 ]; then
    FILE=$1
fi

if [ "$#" -gt 1 ]; then
  echo "ecmcStdLines: Wrong arg count..."
  exit 1  
fi

STD=$(cat ${FILE} | awk -v CONVFMT=%.17g '{s+=$NF; s2+=$NF*$NF;} END {print sqrt((s2/NR)-(s/NR)^2)}')
echo "${STD}"
