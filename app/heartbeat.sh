#!/bin/bash

if [ -z "$RFCAT_PID" ]; then
    echo "RFCAT_PID environment variable is not set."
    exit 1
fi
if [ -z "$ANALYZER_PID" ]; then
    echo "ANALYZER_PID environment variable is not set."
    exit 1
fi


while true; do
    echo "Heart beating..."
    if ps -p $RFCAT_PID > /dev/null; then
        echo "RFCAT is running."
    else
        echo "RFCAT is not running."
    fi
    if ps -p $ANALYZER_PID > /dev/null; then
        echo "ANALYZER is running."
    else
        echo "ANALYZER is not running."
    fi
    
    curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' --user "username:password" http://example.com/api/endpoint
    sleep 60
done
