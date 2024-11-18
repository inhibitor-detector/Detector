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

silence = 0

tempo = 0.203125

initial_beep = [
    (D5, tempo), (silence, tempo/2)
]

error_sound = [
    (B4, tempo), (silence, tempo/2), (B4, tempo), (silence, tempo/2), (B4, tempo), (silence, tempo/2), (B4, tempo), (silence, tempo/2), (B4, tempo), (silence, tempo/2), (B4, tempo), (silence, tempo/2)
]

alarm = [
    (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo), (F5_SHARP, tempo), (B5, tempo)
]

tetris_song_1 = [
    (E5, 2*tempo), (B4, tempo), (C5, tempo), (D5, 2*tempo), (C5, tempo), (B4, tempo), (A4, 2*tempo), (A4, tempo), (C5, tempo), (E5, 2*tempo)
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

def play_sound(sound):
    with alarm_lock:
        tone.start(volume)
        for note, duration in sound:
            play_a_tone(note, duration)
        tone.stop()
        
def play_alarm():
    play_sound(alarm)

def play_initial_beep():
    play_sound(initial_beep)

def play_setup():
    play_sound(tetris_song_1)

def play_error():
    play_sound(error_sound)

play_initial_beep()

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    play_error()
    cleanup()
