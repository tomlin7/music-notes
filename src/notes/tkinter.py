import tkinter as tk

import numpy as np
import pyaudio

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 500  # Amplitude threshold for detecting sound


# Function to get the dominant frequency from audio data
def get_frequency(data):
    windowed_data = np.hamming(len(data)) * data
    fft_data = np.fft.fft(windowed_data)
    fft_freq = np.fft.fftfreq(len(fft_data), 1.0 / RATE)
    positive_freqs = fft_freq[: len(fft_freq) // 2]
    positive_magnitude = np.abs(fft_data[: len(fft_data) // 2])
    dominant_freq = positive_freqs[np.argmax(positive_magnitude)]
    return dominant_freq


# Function to map frequency to musical note
def frequency_to_note(freq):
    if freq <= 0:
        return "No Note"
    A4 = 440.0
    C4 = A4 * 2 ** (-9 / 12)
    semitone = round(12 * np.log2(freq / C4))
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return notes[semitone % 12] + str(semitone // 12 + 4)


# Audio callback function
def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    if np.max(np.abs(audio_data)) < THRESHOLD:
        label_var.set("No Note")
        return (in_data, pyaudio.paContinue)

    freq = get_frequency(audio_data)
    note = frequency_to_note(freq)
    label_var.set(f"Detected Note: {note}")
    return (in_data, pyaudio.paContinue)


# Tkinter setup
root = tk.Tk()

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var, font=("Helvetica", 24))
label.pack(padx=20, pady=20)

# PyAudio setup
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=callback,
)

# Start the stream and Tkinter event loop
stream.start_stream()
root.mainloop()

# Stop and close the stream when exiting
stream.stop_stream()
stream.close()
p.terminate()
