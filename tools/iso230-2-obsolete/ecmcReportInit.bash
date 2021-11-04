#!/bin/bash
# 
# Write first text string to file
#
# Arg 1 report file (output)
# Arg 2 rawdata file
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

if [ "$#" -ne 2 ]; then
   echo "ecmcReportInit: Wrong arg count... Please specify report and rawdata file."
   exit 1 
fi

echo "# ecmc motion system test report" > $1
echo "" >> $1
echo "* Data file   : $2" >> $1
echo "* Date        : $(date)" >> $1
echo "* Author      : $(whoami)" >> $1
echo "" >> $1
