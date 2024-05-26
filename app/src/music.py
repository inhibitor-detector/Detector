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

A5 = 880.0
G5 = 783.99087
F5_SHARP = 739.99
F5 = 698.45646
E5 = 659.25511
D5_SHARP = 622.25397
D5 = 587.32954
C5_SHARP = 554.37
C5 = 523.25113
B4= 493.8833
A4_SHARP = 466.16376
A4 = 440.0
G4_SHARP = 415.3
G4 = 392.0
F4_SHARP = 369.99
F4 = 349.23
E4 = 329.628
D_4_SHARP = 311.13
D4 = 293.66
C4_SHARP = 277.18
C4 = 261.63
B3 = 246.94

# tempo = 0.203125
tempo = 0.40625

# tempo = 0.545

alarm = [
    (A5, tempo), (F5, tempo), (0, tempo/2), (A5, tempo), (F5, tempo), (0, tempo/2), (A5, tempo), (F5, tempo), (0, tempo/2), (A5, tempo), (F5, tempo)
]

tetris_song = [
    (E5, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (C5, tempo), (B4, tempo), (A4, 2*tempo), (A4, tempo), (C5, tempo), (E5, 2*tempo), (D5, tempo), (C5, tempo), (B4, 3*tempo), (C5, tempo), (D5, 2*tempo), (E5, 2*tempo), (C5, 2*tempo), (A4, 2*tempo), (A4, tempo), (A4, tempo), (B4, tempo), (C5, tempo), (D5, 3*tempo), (F5, tempo), (A5, 2*tempo), (G5, tempo), (F5, tempo), (E5, 3*tempo), (C5, tempo), (E5, 2*tempo), (D5, tempo), (C5, tempo), (B4, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (E5, 2*tempo), (C5, 2*tempo), (A4, 2*tempo), (A4, 2*tempo)
]

star_wars_song = [
    (G4, 0.5), (G4, 0.5), (G4, 0.5), (D_4_SHARP, 0.35), (A4_SHARP, 0.15), (G4, 0.5), (D_4_SHARP, 0.35), (A4_SHARP, 0.15), (G4, 1.0), (D5, 0.5), (D5, 0.5), (D5, 0.5), (D5_SHARP, 0.35), (A4_SHARP, 0.15), (F4_SHARP, 0.5), (D_4_SHARP, 0.35), (A4_SHARP, 0.15), (G4, 1.0), (G5, 0.5), (G4, 0.35), (G4, 0.15), (G5, 1.0), (F5_SHARP, 0.5), (F5, 0.35), (E5, 0.15), (D5_SHARP, 1.0), (E5, 0.5), (G4_SHARP, 0.35), (C5_SHARP, 0.15), (C5, 1.0), (B4, 0.5), (A4_SHARP, 0.35), (A4, 0.15), (G4, 1.0), (G5, 0.5), (G4, 0.35), (G4, 0.15), (G5, 1.0), (F5_SHARP, 0.5), (F5, 0.35), (E5, 0.15), (D5_SHARP, 1.0), (E5, 0.5), (G4_SHARP, 0.375), (C5_SHARP, 0.125), (C5, 1.0), (B4, 0.5), (A4_SHARP, 0.375), (A4, 0.125), (G4, 1.0)
]

himno_argentino = [
    (C4, 4*tempo), (E4, 3*tempo), (C4, tempo), (G4, 6*tempo),
    (F4, tempo), (D4, tempo), (B3, 2*tempo), (B3, 2*tempo), (B3, 2*tempo), (B3, 2*tempo),
    (C4, 4*tempo), (D4, 4*tempo), (C4, 4*tempo),
    (C4, 2*tempo),
    (C4, 2*tempo),
    (E4, 2*tempo), (A4, 2*tempo), (G4, 2*tempo), (F4, 2*tempo), (E4, 2*tempo), (D4, 2*tempo),
    (G4, 2*tempo), (E4, 2*tempo), (C4, 2*tempo),
    (F4, 2*tempo), (E4, 2*tempo), (D4, 2*tempo),
    (F4, 2*tempo), (E4, 2*tempo), (D4, 2*tempo),
    (E4, 2*tempo), (F4, 2*tempo), (G4, 2*tempo), (A4, 2*tempo), (B4, 2*tempo), (C5, 2*tempo),
    (D5, 2*tempo), (E5, 2*tempo), (F5, 2*tempo), (G5, 2*tempo),
    (C5, 2*tempo), (D5, 2*tempo), (E5, 2*tempo), (F5_SHARP, 2*tempo), (F5, 2*tempo),
    (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo), (D5, tempo),
    (E4, 2*tempo), (E4, 2*tempo), (G4, 2*tempo), (G4, 2*tempo), (E4, 2*tempo), (E4, 2*tempo), (F4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo), (D4, 2*tempo),
    (F4, 2*tempo), (F4, 2*tempo), (A4, 2*tempo), (A4, 2*tempo), (F4, 2*tempo), (F4, 2*tempo),
    (E4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo),
    (E4, 4*tempo), (E4, 4*tempo), (G4, 4*tempo), (G4, 4*tempo), (E4, 4*tempo), (E4, 4*tempo), (F4, 4*tempo), (D4, 4*tempo), (D4, 4*tempo), (D4, 4*tempo), (D4, 4*tempo), (D4, 4*tempo), (D4, 4*tempo),
    (G4, 4*tempo), (E4, 4*tempo), (E4, 4*tempo), (E4, 4*tempo), (E4, 4*tempo), (E4, 4*tempo),
    (A4, 4*tempo), (F4, 4*tempo), (F4, 4*tempo), (F4, 4*tempo), (F4, 4*tempo), (F4, 4*tempo),
    (B3, 4*tempo), (G4, 4*tempo), (G4, 4*tempo), (G4, 4*tempo), (G4, 4*tempo), (G4, 4*tempo),
    (C4, 4*tempo), (A4, 4*tempo), (A4, 4*tempo), (A4, 4*tempo), (A4, 4*tempo), (A4, 4*tempo),
    (D4, 4*tempo), (B3, 4*tempo), (B3, 4*tempo), (B3, 4*tempo), (B3, 4*tempo), (B3, 4*tempo),
    (E4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo),
    (G4, 4*tempo), (E4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo),
    (E4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo),
    (C4, 4*tempo), (C4, 4*tempo), (C4, 4*tempo)
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

def play_alarm():
    for note, duration in alarm:
        play_a_tone(note, duration)

def play_tetris_theme():
    for note, duration in tetris_song:
        play_a_tone(note, duration)

def play_sw_theme():
    for note, duration in star_wars_song:
        play_a_tone(note, duration)

def play_himno_argentino():
    for note, duration in himno_argentino:
        play_a_tone(note, duration)

try:
    play_alarm()
    # play_tetris_theme()
    # # play_sw_theme()
    # play_himno_argentino()
finally:
    tone.stop()
    GPIO.cleanup()
