#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or use sudo."
  exit 1
fi

filename="./app/logs/log_$(date +'%Y-%m-%d_%H-%M-%S').txt"
touch "$filename"

./app/auto_rfcat.sh >> "$filename" &
export RFCAT_PID=$!
echo "rfcat started"

python ./app/src/main.py $filename &
export PYTHON_PID=$!
echo "python main started"

echo "#!/bin/bash" > stop.sh
echo "kill $RFCAT_PID" >> stop.sh
echo "kill $PYTHON_PID" >> stop.sh

echo "done starting, enjoy!"
exit
