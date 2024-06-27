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
from modules.bot import HarpTabService

def convert_song_to_readable_array(notes):
    readable_array = []
    for note in notes:
        if isinstance(note, list):
            readable_array.append(note[1])
        else:
            readable_array.append(note)
    return readable_array 

def convert_song_notes_to_beautiful_string(notes):
    beautiful_string=""
    for note in notes:
        space = 3
        if isinstance(note, list):
            symbol = note[1]
            beautiful_string+=str(symbol).rjust(space)
            if len(symbol) > 1:
                beautiful_string+=" "
            continue
        tab_len = len(str(note))
        if tab_len >= space:
            space = tab_len + 1

        beautiful_string+=str(note).rjust(space)
    return beautiful_string

def convert_harp_tabs_to_beautiful_string(tabs):
    beautiful_string=""
    for tab in tabs:
        space = 3
        if isinstance(tab, list):
            symbol = tab[1]
            beautiful_string+=str(symbol).rjust(space)
            if len(symbol) > 1:
                beautiful_string+=" "
            continue
        tab_len = len(str(tab))
        if tab_len >= space:
            space = tab_len + 1

        beautiful_string+=str(tab).rjust(space)
    return beautiful_string
