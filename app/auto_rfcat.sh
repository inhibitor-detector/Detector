#!/usr/bin/expect -f

set timeout -1

spawn rfcat -r

expect "(InteractiveConsole)\r\n>>> "

send "d.setFreq(433920000)\n"
expect ">>> "

send "d.discover()\n"
expect "(Press Enter to quit)\r"

set sleep_time [exec bash -c 'source .env && echo $SLEEP']

# Check if sleep_time is a number
if {[string is double $sleep_time]} {
    sleep $sleep_time
} else {
    wait #this command waits for the process to end
}

send "\r"
expect "Exiting Discover mode...\r\n>>> "

send "exit()\n"
expect "====="
