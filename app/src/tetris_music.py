import time
import RPi.GPIO as GPIO

pin_number = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.OUT)

tone = GPIO.PWM(pin_number, 440)
volume = 99

# Define Tetris theme song notes and durations
tetris_notes = [
    (392, 0.5), (392, 0.5), (0, 0.25), (392, 0.5), (294, 0.25), (0, 0.25), (392, 0.5), (523, 0.5), 
    (196, 0.5), (0, 0.25), (196, 0.5), (262, 0.25), (0, 0.25), (196, 0.5), (329, 0.5), 
    (196, 0.5), (0, 0.25), (196, 0.5), (261, 0.25), (0, 0.25), (196, 0.5), (392, 0.5), 
    (0, 0.25), (392, 0.5), (294, 0.25), (0, 0.25), (392, 0.5), (523, 0.5), 
    (196, 0.5), (0, 0.25), (196, 0.5), (262, 0.25), (0, 0.25), (196, 0.5), (329, 0.5), 
    (196, 0.5), (0, 0.25), (196, 0.5), (261, 0.25), (0, 0.25), (196, 1.0),
]

tone.start(volume)

def play_a_tone(freq, duration):
    if freq == 0:
        tone.ChangeDutyCycle(0)
        time.sleep(duration)
    else:
        tone.ChangeFrequency(freq)
        tone.ChangeDutyCycle(volume)
        time.sleep(duration)

def play_tetris_theme():
    for note, duration in tetris_notes:
        print("playing ", note)
        play_a_tone(note, duration)

try:
    play_tetris_theme()
finally:
    tone.stop()
    GPIO.cleanup()
