import time
import RPi.GPIO as GPIO
# import board

pin_number = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.OUT)

tone = GPIO.PWM(pin_number, 440)
volume = 1
# tone.duty_cycle = volume

tone.start(volume)

input('Press return to stop:')

tone.stop()
GPIO.cleanup()

# notes = [262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523]
# tone_duration = 0.5
# rest_duration = 0.1

# def play_a_tone(freq, duration):
#     tone.duty_cycle = volume
#     tone.frequency = freq
#     time.sleep(duration)

# def play_a_rest(duration):
#     tone.duty_cycle = 0
#     time.sleep(duration)

# for note in notes:
#     print("playing ", note)
#     play_a_tone(note, tone_duration)
#     play_a_rest(rest_duration)
    