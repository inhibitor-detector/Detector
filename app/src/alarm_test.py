import RPi.GPIO as GPIO
from gpiozero import Buzzer
import time

pin_number = 1
buzzer = Buzzer (pin_number) 
buzzer.on()
time.sleep(2)
buzzer.off()
