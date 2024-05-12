import time
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

pin_number = 1

# # Set up GPIO
# GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
# GPIO.setup(pin_number, GPIO.OUT)  # Set GPIO pin_number as output

# while True:
#     print("Beep")
#     GPIO.output(pin_number, True)  # Turn on the speaker
#     time.sleep(1)  # Play the beep for 100ms
#     GPIO.output(pin_number, False)  # Turn off the speaker

bz = Buzzer(pin_number)
bz.on()
while True:
    print("Beep")
    bz.beep()
    time.sleep(1)



bz = TonalBuzzer(pin_number)

b.play(Tone("A4"))

b.play(Tone(220.0)) # Hz

b.play(Tone(60)) # middle C in MIDI notation

b.play("A4")

b.play(220.0)

b.play(60)