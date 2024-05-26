import time
import RPi.GPIO as GPIO

pin_number = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_number, GPIO.OUT)

tone = GPIO.PWM(pin_number, 440)
volume = 99

B5 = 987.77
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

tempo = 0.203125

alarm = [
    (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo)
]

tetris_song = [
    (E5, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (C5, tempo), (B4, tempo), (A4, 2*tempo), (A4, tempo), (C5, tempo), (E5, 2*tempo), (D5, tempo), (C5, tempo), (B4, 3*tempo), (C5, tempo), (D5, 2*tempo), (E5, 2*tempo), (C5, 2*tempo), (A4, 2*tempo), (A4, tempo), (A4, tempo), (B4, tempo), (C5, tempo), (D5, 3*tempo), (F5, tempo), (A5, 2*tempo), (G5, tempo), (F5, tempo), (E5, 3*tempo), (C5, tempo), (E5, 2*tempo), (D5, tempo), (C5, tempo), (B4, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (E5, 2*tempo), (C5, 2*tempo), (A4, 2*tempo), (A4, 2*tempo)
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

def play():
    try:
        play_alarm()
        # play_tetris_theme()
    finally:
        tone.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    play()
