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
from enum import Enum

# TODO: layouts should be outsourced to files with no enum
class Layout(Enum):
    Major_Diatonic = 1
    Natural_Minor = 2
    Harmonic_Minor = 3
    Melody_Maker = 4
    Chromatic = 5
    Steel_Tongue_Major_13 = 100

harp_layout_10_holes_major={
    "layout": Layout.Major_Diatonic,
    "name": "Diatonic Major",
    "type": "Diatonic",
    "blows": [48, 52, 55, 60, 64, 67, 72, 76, 79, 84],
    "draws": [50, 55, 59, 62, 65, 69, 71, 74, 77, 81],
    "bending_corrections": {
        'blows': [0, 0, 0, 0, 0, 0, 0, 1, 1, 2], 
        'draws': [1, 2, 3, 1, 0, 1, 0, 0, 0, 0]
    }
}

harp_layout_10_holes_harmonic_minor={
    "layout": Layout.Harmonic_Minor,
    "name": "Harmonic Minor",
    "type": "Diatonic",
    "blows": [48, 51, 55, 60, 63, 67, 72, 75, 79, 84],
    "draws": [50, 55, 59, 62, 65, 68, 71, 74, 77, 80],
    "bending_corrections": {
        'blows': [0, 0, 0, 0, 0, 0, 0, 0, 1, 3], 
        'draws': [1, 3, 3, 1, 1, 0, 0, 0, 0, 0]
    }
}

harp_layout_10_holes_natural_minor={
    "layout": Layout.Natural_Minor,
    "name": "Natural Minor",
    "type": "Diatonic",
    "blows": [60, 63, 67, 72, 75, 79, 84, 87, 91, 96],
    "draws": [62, 67, 70, 74, 77, 81, 82, 86, 89, 93],
    "bending_corrections": {
        'blows': [0, 0, 0, 0, 0, 0, 1, 0, 1, 2], 
        'draws': [1, 3, 2, 1, 1, 1, 0, 0, 0, 0]
    } 
}

harp_layout_10_holes_melody_maker={
    "layout": Layout.Melody_Maker,
    "name": "Melody Maker",
    "type": "Diatonic",
    "blows": [48, 52, 57, 60, 64, 67, 72, 76, 79, 84],
    "draws": [50, 55, 59, 62, 66, 69, 71, 74, 78, 81],
    "bending_corrections": {
        'blows': [0, 0, 0, 0, 0, 0, 0, 1, 0, 2], 
        'draws': [1, 2, 1, 1, 1, 1, 0, 0, 0, 0]}
}

harp_layout_12_holes_chromatic={
    "layout": Layout.Chromatic,
    "name": "Chromatic",
    "type": "Chromatic",
    "blows": [48, 52, 55, 60, 60, 64, 67, 72, 72, 76, 79, 84],
    "draws": [50, 53, 57, 59, 62, 65, 69, 71, 74, 77, 81, 83]
}

steel_tongue_13_tones_major={
    "layout": Layout.Steel_Tongue_Major_13,
    "name": "Steel Tongue Drum Major 13",
    "type": "Drum",
    "blows": [0, 0, 57, 60, 64, 67, 72, 76, 0, 0],
    "draws": [0, 55, 59, 62, 65, 69, 71, 74, 0, 0],
    "tabs_mapping": {
        "-2": "5-",
        "3": "6-",
        "-3": "7-",
        "4": "1",
        "-4": "2",
        "5": "3",
        "-5": "4",
        "6": "5",
        "-6":"6",
        "-7": "7",
        "7": "1+",
        "-8": "2+",
        "8": "3+"
    }
}

Harp_Layouts = {
    Layout.Major_Diatonic: harp_layout_10_holes_major,
    Layout.Natural_Minor: harp_layout_10_holes_natural_minor,
    Layout.Harmonic_Minor: harp_layout_10_holes_harmonic_minor,
    Layout.Melody_Maker: harp_layout_10_holes_melody_maker,
    Layout.Chromatic : harp_layout_12_holes_chromatic, 
    Layout.Steel_Tongue_Major_13: steel_tongue_13_tones_major
}
