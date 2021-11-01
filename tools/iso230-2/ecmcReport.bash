#!/bin/bash
# 
# Write text string to file
#
# Arg 1 report file (output)
# Arg 2 Text string
#
# Author: Anders Sandström, anders.sandstrom@esss.se
#

if [ "$#" -ne 2 ]; then
   echo "main: Wrong arg count... Please specify input and output file."
   exit 1 
fi

echo $2 >> $1
