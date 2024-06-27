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
from modules.notes import ABCNotationImporter
from modules.notes import UserInputNotesParser
from modules.engine import HarpLayout
from modules.engine import HarpConverter
from datetime import datetime

def _getDateTime():
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime

def _addLayoutScoreToSong(song):
    song["layout_scores"] = {}

    for harp_layout in HarpLayout.Layout:
        harp = HarpLayout.Harp_Layouts[harp_layout]
        best_tabs = HarpConverter.searchBestTabsForSong(song["notes"], harp, 60)
        if len(best_tabs) > 0:
            song["layout_scores"][harp_layout.name] = best_tabs[0]["stats"]

def _getSongTemplate(creator_id, source):
    return {
        "creator": creator_id,
        "date": _getDateTime(),
        "source": source
    }

def createSongByUserInput(creator_id, song_title, song_key, user_input_string):
    song = _getSongTemplate(creator_id, "user_input")
    song["title"] = song_title
    song["key"] = song_key
    song["notes"] = UserInputNotesParser.convert_user_input_notes(user_input_string, song_key)
    song["raw"] = user_input_string
    _addLayoutScoreToSong(song)
    return song


def createSongsByABCNotationCom(creator_id, url):
    songs = []
    fetched_songs = ABCNotationImporter.fetch_from_abcnotationcom(url)
    for fetched_song in fetched_songs:
        song = _getSongTemplate(creator_id, "abcnotation")
        song["url"] = url
        song["title"] = fetched_song["title"]
        song["notes"] =  fetched_song["notes"]
        _addLayoutScoreToSong(song)
        songs.append(song)
    return songs

def createSongByTabs(creator_id, song_title, raw_tab_string):
    song = _getSongTemplate(creator_id, "tabs")
    song["title"] = song_title
    song["tabs"] = raw_tab_string
    return song
