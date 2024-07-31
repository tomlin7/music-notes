# import mido
# from pydub import AudioSegment


# def midi_to_audio(midi_file, output_file):
#     mid = mido.MidiFile(midi_file)
#     audio = AudioSegment.from_raw(
#         mid.synthesize(), sample_width=2, frame_rate=44100, channels=2
#     )
#     audio.export(output_file, format="wav")


# midi_file = "your_midi_file.mid"
# output_file = "output.wav"
# midi_to_audio(midi_file, output_file)

import random

from music21 import *

notes = []
bpm = 120
music21_notes = []
for note_name, _ in notes:
    if note_name:
        music21_note = note.Note(note_name)
        # music21_note.duration.quarterLength = duration * 60 / bpm
        music21_notes.append(music21_note)
    else:
        rest = note.Rest()
        # rest.duration.quarterLength = duration * 60 / bpm
        music21_notes.append(rest)

stream = stream.Stream()

for music21_note in music21_notes:
    stream.append(music21_note)


sp = midi.realtime.StreamPlayer(stream)
sp.play()

# b = corpus.parse("bach/bwv66.6")
# for n in b.flatten().notes:
#     n.microtone = keyDetune[n.pitch.midi]
# sp = midi.realtime.StreamPlayer(b)
# sp.play()
