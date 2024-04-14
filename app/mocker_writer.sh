#!/bin/bash

echo HELLO I AM MOCK WRITER

# Check if the logs file argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <logs_file>"
    exit 1
fi

# Get the logs file from the command-line argument
logs_file="$1"

while true; do
    sleep 5
    echo "ffffffffffff" > $logs_file
done