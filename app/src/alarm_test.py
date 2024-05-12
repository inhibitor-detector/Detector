import RPi.GPIO as GPIO
# from gpiozero import Buzzer
import time

pin_number = 1

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(pin_number, GPIO.OUT)  # Set GPIO pin_number as output

while True:
    print("Beep")
    GPIO.output(pin_number, True)  # Turn on the speaker
    time.sleep(1)  # Play the beep for 100ms
    GPIO.output(pin_number, False)  # Turn off the speaker