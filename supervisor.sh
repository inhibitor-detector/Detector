#!/bin/bash

# Function to get PIDs from stop.sh
get_pids() {
    rfcat_pid=$(grep -oP "kill \K\d+" stop.sh | head -n 1)  # First PID for rfcat
    python_pid=$(grep -oP "kill \K\d+" stop.sh | tail -n 1)  # Second PID for Python
}

./start.sh &

sleep 30

get_pids

# Main monitoring loop
while true; do
    # Check if the Python process is running
    if ! ps -p $python_pid > /dev/null; then
        echo "Python process with PID $python_pid is not running. Restarting..."
        
        # Run make restart to kill and restart the processes
        make restart
        
        # After restart, get the new PIDs
        get_pids
    fi
    
    # Check if the rfcat process is running
    if ! ps -p $rfcat_pid > /dev/null; then
        echo "rfcat process with PID $rfcat_pid is not running. Restarting..."
        
        # Run make restart to kill and restart the processes
        make restart
        
        # After restart, get the new PIDs
        get_pids
    fi
    
    sleep 10
done

