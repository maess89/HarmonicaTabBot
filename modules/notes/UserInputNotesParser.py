# Harmonica Tab Bot
# Copyright (C) 2024 maess89
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from music21 import note as mnote
from music21 import key as mkey
import modules.notes.MidiConverter as MidiConverter

def adjust_notes_octaves_to_C_tonic_based_notation(notes, key_signature):
    key_from = mkey.Key(key_signature).tonic.name
    key_to = "C"
    midi_pitches_from_to= MidiConverter.convertNotesToMidiPitches([key_from, key_to])

    adjusted_notes = []
    for note in notes:
        if isinstance(note, list):
            adjusted_notes.append(note)
            continue
        current_note = mnote.Note(note).pitch
        current_key = current_note.name
        current_octave = current_note.octave
        current_key_pitch = MidiConverter.convertNotesToMidiPitches([current_key])[0] 
        if midi_pitches_from_to[1] <= current_key_pitch and current_key_pitch < midi_pitches_from_to[0]:
            current_octave=current_octave+1
        adjusted_notes.append("{}{}".format(current_key, current_octave))
    return adjusted_notes

def convert_user_input_notes(notes_str, key_signature=None):
    notes = []
    note_lines = notes_str.split("\n")
    for line in note_lines:
        tokens_in_line = line.split(" ")
        for token in tokens_in_line:
            note=None
            try:
                m21note = mnote.Note(token)
                note = m21note.pitch.name
                octave = m21note.pitch.octave
                if octave == None:
                    octave =4
                elif octave == 0:
                    octave = 3
                elif octave == 1:
                    octave = 4
                elif octave == 2:
                    octave = 5
                elif octave == 3:
                     octave = 6
                note="{}{}".format(note, octave)
            except:
                pass
            if note is None:
                notes.append(["symbol", token])
            else:
                notes.append(note)
        if len(note_lines) > 1:
            notes.append(["symbol", "\n"])
    if key_signature is not None:
        notes = adjust_notes_octaves_to_C_tonic_based_notation(notes, key_signature)
    return notes