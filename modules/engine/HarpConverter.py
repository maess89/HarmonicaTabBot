
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
import modules.engine.HarpTabUtils as HarpTabUtils
import modules.engine.HarpLayout as HarpLayout
import modules.notes.MidiConverter as MidiConverter
import statistics
import math

INCLUDE_BENDING=True
BEND_CHARACTER="b"
SLIDE_CHARACTER="#"

def vector_to_string(harp_holes_lines):
    overall_string=""
    for line in harp_holes_lines:
        line_str=""
        for note in line:
            line_str+=str(note).rjust(4)+" "
        overall_string+=line_str+"\n"
    return overall_string

def getTabStatistics(tabs):
	statistics = {
		"total":0,
		"bends":0,
		"unknowns":0,
        "slides": 0
	}
	for tab in tabs:
		if isinstance(tab, list):
			continue
		if tab == "?":
			statistics["unknowns"]+=1
		if BEND_CHARACTER in str(tab):
			statistics["bends"]+=1
		if SLIDE_CHARACTER in str(tab):
			statistics["slides"]+=1
        
		statistics["total"]+=1
	return statistics


def resolveTabHoleViaBending(song_note_midi_pitch, midi_pitch_blows, midi_pitch_draws, bending_corrections):
    match_index = -1
    pitch_shifted = 0
    for i in range(0, len(bending_corrections["blows"])):
        bending_correction_blow = bending_corrections["blows"][i]
        bending_corrections_draw = bending_corrections["draws"][i]
        
        for pitch_shift in range(1, bending_correction_blow+1):
            if song_note_midi_pitch == midi_pitch_blows[i] - pitch_shift:
                match_index = i
                match_is_blow = True
                pitch_shifted=pitch_shift

        if match_index >= 0:
            break

        for pitch_shift in range(1, bending_corrections_draw+1):
            if song_note_midi_pitch == midi_pitch_draws[i] - pitch_shift:
                match_index = i
                match_is_blow = False
                pitch_shifted=pitch_shift
    if match_index>=0:
        sign=""
        if not match_is_blow:
            sign="-"
        register=match_index+1
        return "{}{}{}{}".format(sign, register, BEND_CHARACTER, "."*pitch_shifted)
    return None


def resolveTabHoleViaChromaticSlide(song_note_midi_pitch, midi_pitch_blows, midi_pitch_draws):
    match_index = -1
    pitch_shift = 1
    for i in range(0, len(midi_pitch_blows)):
        if song_note_midi_pitch == midi_pitch_blows[i] + pitch_shift:
            match_index = i
            match_is_blow = True

        if match_index >= 0:
            break

        if song_note_midi_pitch == midi_pitch_draws[i] + pitch_shift:
            match_index = i
            match_is_blow = False
    if match_index>=0:
        sign=""
        if not match_is_blow:
            sign="-"
        register=match_index+1
        return "{}{}{}".format(sign, register, SLIDE_CHARACTER)
    return None

def findTabHole(harp_layout, song_note_midi_pitch, midi_pitch_blows, midi_pitch_draws):
    match_index = -1
    match_is_blow = True
    for i in range(0, len(midi_pitch_blows)):
        # TODO: Hole search is not optimal for layouts with duplicate pitches, e.g. -2 & 3 on a diatonic major
        # It would be better to compare the matches against the previous hole in order to prefer the closer one
        if song_note_midi_pitch == midi_pitch_blows[i]:
            match_index = i
            match_is_blow = True
        if song_note_midi_pitch == midi_pitch_draws[i]:
            match_index = i
            match_is_blow = False
    if match_index>0:
        sign=""
        if not match_is_blow:
            sign="-"
        register=match_index+1
        return "{}{}".format(sign, register)
    else:
        tab_via_bending = None
        layout_type = harp_layout["type"]
        if layout_type == "Diatonic":
            bending_corrections = harp_layout["bending_corrections"]
            tab_via_bending = resolveTabHoleViaBending(song_note_midi_pitch, midi_pitch_blows, midi_pitch_draws, bending_corrections)
        elif layout_type == "Chromatic":
            tab_via_bending = resolveTabHoleViaChromaticSlide(song_note_midi_pitch, midi_pitch_blows, midi_pitch_draws)
        if tab_via_bending is not None:
            return tab_via_bending
    return "?"

def createTabsForSong(song_notes, harp_layout, pitch_offset=0):
    midi_pitch_blows, midi_pitch_draws = harp_layout["blows"], harp_layout["draws"]

    tabs = []
    for note in song_notes:
        if isinstance(note, list):
            tabs.append(note)
            continue
        song_note_midi_pitch = MidiConverter.convertNotesToMidiPitches([note])[0]+pitch_offset
        tab_hole = findTabHole(harp_layout, song_note_midi_pitch, midi_pitch_blows, midi_pitch_draws)
        tabs.append(tab_hole)

    # Convert Tabs for Steel Tongue Notes
    if harp_layout["layout"] == HarpLayout.Layout.Steel_Tongue_Major_13:
        final_tabs = []
        for tab_symbol in tabs:
            if not isinstance(tab_symbol, list):
                if tab_symbol != "?":
                    final_tabs.append(harp_layout["tabs_mapping"][tab_symbol])
                else:
                    final_tabs.append(tab_symbol)
            else:
                final_tabs.append(tab_symbol)
        tabs = final_tabs
    return tabs

def calcTabScore(tab_stats, bending):
    bend_multiplicator=2
    if bending:
        bend_multiplicator=1
    bad_things = tab_stats["unknowns"]*2 + tab_stats["bends"]*bend_multiplicator
    if "slides" in tab_stats:
        bad_things += tab_stats["slides"]*0.25
    score = 100. - (bad_things/float(tab_stats["total"])*100.)
    if score < 0:
        score = 0
    return score

def sortTabsByScore(tab_candidates, bending, limit=3):
    tab_candidates = sorted(tab_candidates, key=lambda x: -calcTabScore(x["stats"], bending))
    if limit is not None:
        tab_candidates = tab_candidates[:limit]
    return tab_candidates

def _getMidiPitchArrayOfSong(song_notes):
    pitch_array = []
    for song_note in song_notes:
        if isinstance(song_note, list):
            continue
        pitch_array.append(MidiConverter.convertNotesToMidiPitches([song_note])[0])
    return pitch_array

def _getMidiPitchArrayOfLayout(harp_layout):
    pitch_array = []
    pitch_array.extend(harp_layout["blows"])
    pitch_array.extend(harp_layout["draws"])
    # remove 0s for layouts which uses them as padding, e.g steel drum
    # TODO: in future it is better to support dynamic layouts
    return [num for num in pitch_array if num != 0]

def searchBestTabsForSong(song_notes, layout, bending=False, limit=3):
    # 1. get midi pitch array of song
    pitches_song = _getMidiPitchArrayOfSong(song_notes)

    # 2. get midi pitch array of harp layout
    pitches_harp = _getMidiPitchArrayOfLayout(layout)

    # 3. get mean of harp layout, get mean of song MEAN_SONG
    mean_song = statistics.mean(pitches_song)
    mean_harp = statistics.mean(pitches_harp)

    # 4. calculate the difference OFFSET of mean bet. harp layout & song
    offset_harp_song =mean_harp - mean_song

    offset_min_to_mean_song = min(pitches_song) - mean_song
    offset_max_to_mean_song = max(pitches_song) - mean_song

    # 6. get difference of lowest (LOWEST_NOTE_OFFSET) and highstes pitch (HIGHEST_NOTE_OFFSET) of song to its mean MEAN_SONG
    # 7. shift now the song as follows: song + OFFSET + [LOWEST_NOTE_OFFSET, ..-1, 0, 1, ., HIGHEST_NOTE_OFFSET]
    tab_candidates = []

    # calc pitch shift boundaries
    start = math.floor(offset_min_to_mean_song) 
    end = math.ceil(offset_max_to_mean_song)    
    last_tabs = None
    for pitch_shift in range(start, end + 1):
        pitch_offset = int(offset_harp_song + pitch_shift)
        tabs = createTabsForSong(song_notes, layout, pitch_offset)
        tabs_stats = getTabStatistics(tabs)
        # skip duplicate tabs
        if tabs == last_tabs:
            continue
        tab_candidates.append({"tabs": tabs, "stats": tabs_stats, "harp_layout": layout})
        last_tabs = tabs
   
    tab_candidates=sortTabsByScore(tab_candidates, bending, limit=limit)
    if limit is not None:
        tab_candidates = tab_candidates[:limit]
    return tab_candidates

def searchBestTabsForSongOverLayouts(song_notes, layouts, bending=True, limit=3):
    tab_candidates=[]
    for layout in layouts:
        harp = HarpLayout.Harp_Layouts[layout]
        best_tabs = searchBestTabsForSong(song_notes, harp, limit=None)
        tab_candidates.extend(best_tabs)
        
    tab_candidates=sortTabsByScore(tab_candidates, bending, limit=limit)
    return tab_candidates