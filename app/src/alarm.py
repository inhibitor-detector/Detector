import time
import RPi.GPIO as GPIO
import threading

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
    (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo)
]
tetris_song_1 = [
    (E5, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (C5, tempo), (B4, tempo), (A4, 2*tempo), (A4, tempo), (C5, tempo), (E5, 2*tempo)
]

tetris_song_2 = [
    (D5, tempo), (C5, tempo), (B4, 3*tempo), (C5, tempo), (D5, 2*tempo), (E5, 2*tempo), (C5, 2*tempo), (A4, 2*tempo), (A4, tempo)
    # (A4, tempo), (B4, tempo), (C5, tempo), (D5, 3*tempo), (F5, tempo), (A5, 2*tempo), (G5, tempo), (F5, tempo), (E5, 3*tempo), (C5, tempo), (E5, 2*tempo), (D5, tempo), (C5, tempo), (B4, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (E5, 2*tempo), (C5, 2*tempo), (A4, 2*tempo), (A4, 2*tempo)
]

#hardcoded is simpler, no need to parametrize IO pins
gnd_pin = 6 
gpio_pin = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio_pin, GPIO.OUT)

tone = GPIO.PWM(gpio_pin, 440)
volume = 99

alarm_lock = threading.Lock()

def play_a_tone(freq, duration):
    if freq == 0:
        tone.ChangeDutyCycle(0)
        time.sleep(duration)
    else:
        tone.ChangeFrequency(freq)
        tone.ChangeDutyCycle(volume)
        time.sleep(duration)

def play_alarm():
    with alarm_lock:
        for note, duration in alarm:
            play_a_tone(note, duration)

def play_setup():
    with alarm_lock:
        for note, duration in tetris_song_1:
            play_a_tone(note, duration)

def play():
    try:
        tone.start(volume)
        play_alarm()
    finally:
        tone.stop()

try: 
    tone.start(volume)
    play_setup()
finally:
    tone.stop()


def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    play()
    cleanup()
