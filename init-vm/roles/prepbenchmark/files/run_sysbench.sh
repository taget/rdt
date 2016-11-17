#!/bin/bash
# author Eli Qiao

# stream is from https://www.cs.virginia.edu/stream/ref.html
# and build by gcc -O stream.c -o stream
# just let it run for ever which works as a noisy process
# 
LOG=/tmp/stream.log
while true ; do
    RES=$(/tmp/stream)
    date >> $LOG
    echo "------------------------" >> $LOG
    echo $RES >> $LOG
done
