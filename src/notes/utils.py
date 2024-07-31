import numpy as np

from .constants import *


def get_frequency(data):
    windowed_data = np.hamming(len(data)) * data
    fft_data = np.fft.fft(windowed_data)
    fft_freq = np.fft.fftfreq(len(fft_data), 1.0 / RATE)
    positive_freqs = fft_freq[: len(fft_freq) // 2]
    positive_magnitude = np.abs(fft_data[: len(fft_data) // 2])

    cutoff = 2000  # Hz
    mask = positive_freqs < cutoff
    filtered_magnitude = positive_magnitude * mask

    dominant_freq = positive_freqs[np.argmax(filtered_magnitude)]
    return dominant_freq


def frequency_to_note(freq):
    if freq <= 0:
        return "No Note"

    semitone = round(12 * np.log2(freq / C4))
    note = NOTES[semitone % 12] + str(semitone // 12 + 4)

    return note
