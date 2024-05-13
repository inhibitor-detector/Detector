import time
import RPi.GPIO as GPIO

pin_number = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.OUT)

tone = GPIO.PWM(pin_number, 440)
volume = 99

# Define Tetris theme song notes and durations
A = 440
B = 494
C = 523
D = 587
E = 659

tetris_notes = [
    (E, 0.5), (B, 0.5), (C, 0.5), (D, 0.5), (C, 0.5), (B, 0.5), (A, 0.5), (A, 0.5),
    (C, 0.5), (E, 0.5), (D, 0.5), (C, 0.5), (B, 0.5), (C, 0.5), (D, 0.5), (E, 0.5),
    (C, 0.5), (A, 0.5), (A, 0.5), (A, 0.5), (A, 0.5), (B, 0.5), (C, 0.5), (D, 0.5),
    (E, 0.5), (C, 0.5), (B, 0.5), (A, 0.5), (A, 0.5), (A, 0.5), (A, 0.5), (C, 0.5),
    (E, 0.5), (D, 0.5), (C, 0.5), (B, 0.5), (C, 0.5), (D, 0.5), (E, 0.5), (C, 0.5),
    (A, 0.5), (A, 0.5), (A, 0.5), (A, 0.5), (B, 0.5), (C, 0.5), (D, 0.5), (E, 0.5),
    (C, 0.5), (B, 0.5), (A, 0.5)
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
