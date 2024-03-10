#!/usr/bin/expect -f

spawn rfcat -r

expect "(InteractiveConsole)\r\n>>> "

send "d.setFreq(433920000)\n"
expect ">>> "

send "d.discover()\n"
expect "(Press Enter to quit)\r"


sleep 10

send "\r"
expect "Exiting Discover mode...\r\n>>> "
#expect ">>> "
send "exit()\n"
expect "====="

#interact #this command hands control to the user

#wait #this command waits for the process to end?

