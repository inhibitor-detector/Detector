#!/bin/bash

filename="./app/logs/log_$(date +'%Y-%m-%d_%H-%M-%S').txt"
touch "$filename"

# "&" is to run in parallel
#tee allows to write to a file but also show in STO
# ./auto_rfcat.sh | tee "$filename" &
./app/auto_rfcat.sh >> "$filename" &
export RFCAT_PID=$!

./app/analyzer.py $filename &
export ANALYZER_PID=$!

./app/heartbeat.py &
export HEARTBEAT_PID=$!

wait

echo "done, bye!"
exit
