import time
import RPi.GPIO as GPIO
import board
import pwmio

tone = GPIO.PWM(board.GP15, 440)#variable_frequency=True)
volume = 99
# tone.duty_cycle = volume

tone.start(volume)

time.sleep(10)

tone.stop()

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
    