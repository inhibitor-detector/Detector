#!/usr/bin/expect -f

set timeout -1

spawn rfcat -r

expect "(InteractiveConsole)\r\n>>> "

send "d.setFreq(433920000)\n"
expect ">>> "

send "d.discover()\n"
expect "(Press Enter to quit)\r"

# TODO
# if SLEEP var in .env is a number, wait those seconds, else wait indefinetly by doing expect "string that will not appear"
# to wait indefinetly we could also experiment with the "wait" command,
# if {[string match "some_condition" $expect_out(buffer)]} {
#     send "do_something\r"
# } else {
#     send "do_something_else\r"
# }

sleep 60

send "\r"
expect "Exiting Discover mode...\r\n>>> "

send "exit()\n"
expect "====="

#interact #this command hands control to the user

#wait #this command waits for the process to end?

