#!/bin/bash
# 
# Calc average of camonitor text lines
#
# Arg 1 Optional file name, otherwise stdin
#
# Return Average value.
#
# Example: Avg all lines from stdin with 10
# bash ecmcAvgData.bash
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

FILE="-"
if [ "$#" -eq 1 ]; then
    FILE=$1
fi

if [ "$#" -gt 1 ]; then
  echo "ecmcAvgLines: Wrong arg count..."
  exit 1  
fi

AVG=$(cat ${FILE} | awk -v CONVFMT=%.17g '{sum+=$NF} END {print sum/NR}')
echo "${AVG}"
