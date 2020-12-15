#!/bin/bash
# 
# Calc range of elements in a row
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Range value
#
# Example: Avg values in a row
# bash ecmcAvgData.bash
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

FILE="-"
if [ "$#" -eq 1 ]; then
    FILE=$1
fi

if [ "$#" -gt 1 ]; then
  echo "ecmcAvgDataRow: Wrong arg count..."
  exit 1  
fi

RANGE=$(cat ${FILE} | awk '{max=$1; min=$1; for (i = 1; i <= NF; i++){if($i>max){max=$i};if($i<min){min=$i}} ; print max-min}')
echo "${RANGE}"
