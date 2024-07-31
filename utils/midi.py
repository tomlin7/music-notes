from music21 import *

notes = [(note_name, 0.5) for note_name in ["C4", "E4", "G4", "C5"]]

stream = stream.Stream()

for pitch, duration in notes:
    note = note.Note(pitch)
    note.duration.quarterLength = duration
    stream.append(note)

# sp = midi.realtime.StreamPlayer(stream)
# sp.play()

stream.write("midi", "output.mid")
