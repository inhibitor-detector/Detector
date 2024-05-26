#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or use sudo."
  exit 1
fi

filename="./app/logs/log_$(date +'%Y-%m-%d_%H-%M-%S').txt"
touch "$filename"

# "&" is to run in parallel
#tee allows to write to a file but also show in STO
# ./auto_rfcat.sh | tee "$filename" &
./app/auto_rfcat.sh >> "$filename" &
export RFCAT_PID=$!
echo "rfcat started"

# ./app/analyzer.py $filename &
# export ANALYZER_PID=$!

# ./app/heartbeat.py &
# export HEARTBEAT_PID=$!

python ./app/src/main.py $filename &
echo "python main started"

# wait # TODO this does busy waiting i think

echo "done starting, enjoy!"
exit
