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
import requests
import partitura as pt
import re
from modules.notes import MidiConverter

def read_music_xml(music_xml_filename):
    loaded_musicxml = pt.load_musicxml("resources/import/musicxml/"+music_xml_filename)
    the_key = pt.musicanalysis.estimate_key(loaded_musicxml)
    note_array = loaded_musicxml.note_array(include_time_signature=False)
    voices_of_note=pt.musicanalysis.estimate_voices(loaded_musicxml[0], monophonic_voices = True)

    load_voice_only = 1
    parsed_notes = []
    for idx, midi_note in enumerate(note_array):
        if idx < len(voices_of_note):
            if voices_of_note[idx] == load_voice_only:
                key=str(midi_note[6])
                parsed_notes.append(MidiConverter.convertMidiPitchesToNotes([int(key)])[0])
    return {
        "title": music_xml_filename[:music_xml_filename.rfind(".")],
        "notes": parsed_notes
    }

def fetch_from_abcnotationcom(url="https://abcnotation.com/tunePage?a=pghardy.net/tunebooks/pgh_session_tunebook/0243"):
    content =  response = requests.get(url).text

    xml_links =  re.findall(r'href=["\'](.*?\.xml\?a=.*?)["\']', content)
    songs = []
    for xml_link in xml_links:
        response = requests.get("https://abcnotation.com/"+xml_link)
        title = xml_link.split(".xml")[0].split("/")[-1]
        file = title +".musicxml"
        with open("resources/import/musicxml/"+file, 'wb') as f:
            f.write(response.content)
        song = read_music_xml(file)
        songs.append(song)

    return songs