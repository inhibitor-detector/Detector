#!/bin/bash

echo HELLO I AM ANALYZER

# Check if the logs file argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <logs_file>"
    exit 1
fi

# Get the logs file from the command-line argument
logs_file="$1"

if [ -f "$logs_file" ]; then
    # Use tail to read the last few lines of the logs file
    tail -f "$logs_file" | while IFS= read -r line; do
        # Perform simple analysis on each line
        if [[ "$line" == *"ffffff"* ]]; then
            echo "Inhibitor detected"
        fi

        if [[ "$line" == *"exit()"* ]]; then #exit manually by dev or automatically when rfcat finishes
            echo "Exit"
            exit
        fi
    done
else
    echo "Error: The logs file '$logs_file' does not exist."
fi
