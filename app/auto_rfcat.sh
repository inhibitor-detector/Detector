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

# Load the .env variable
set sleep_time [exec bash -c 'source .env && echo $SLEEP']

# Check if sleep_time is a number
if {[string is double $sleep_time]} {
    puts "Waiting x seconds"
    puts $sleep_time
    sleep $sleep_time
} else {
    puts "Waiting indefinitely..."
    expect "string that will not appear" # Wait indefinitely
}

send "\r"
expect "Exiting Discover mode...\r\n>>> "

send "exit()\n"
expect "====="

#wait #this command waits for the process to end?
