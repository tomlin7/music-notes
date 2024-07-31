import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 500  # Amplitude threshold for detecting sound

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

A4 = 440.0
C4 = A4 * 2 ** (-9 / 12)
