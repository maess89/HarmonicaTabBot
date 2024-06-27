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
from music21 import pitch as mpitch

def convertNotesToMidiPitches(notes):
    midi_numbers = [ int(mnote.Note(note).pitch.midi) for note in notes]
    return midi_numbers

def convertMidiPitchesToNotes(midi_pitches):
    notes = []
    for midi_pitch in midi_pitches:
        mpitch_object = mpitch.Pitch(midi=midi_pitch)
        note = mpitch_object.name + str(mpitch_object.octave)
        notes.append(note)
    return notes
