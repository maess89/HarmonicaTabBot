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
from modules.notes import NotesImporter
from modules.engine import HarpConverter
from modules.engine import HarpLayout
from modules.config.UserConfig import UserConfigManager
from modules.bot import HarpTabBotUserSession
from modules.bot import HarpTabBot_Localization
import modules.songs.Songs as Songs
import random

VERBOSE = True
userConfigManager = UserConfigManager()

localizations = {
	"de": HarpTabBot_Localization.Localization(lang='de'),
	"en": HarpTabBot_Localization.Localization(lang='en') 
}

def getSongList(userSession, filter = None):
    songBook = userSession.getSongBook()
    songList = []
    index=0
    for song in songBook.get_songs_titles():
        append = filter is None
        if filter is not None:
            filterWords = []
            if " " in filter:
                filterWords = filter.split(" ")
            else:
                filterWords.append(filter)
            for filterWord in filterWords:
                append = filterWord.lower() in song.lower()
        if append:
            songList.append({
                "index": index,
                "title": song
            })
        index+=1
    return songList

def getSongListAndFilterByKeywords(userSession, keywords):
	# TODO: check difference to filter in getSongList
	songs = getSongList(userSession, filter = None)
	songs_to_return =[]
	if len(keywords) > 2:
		songs_to_return = []
		for song in songs:
			song_title = song["title"]
			if keywords.lower() in song_title.lower():
				songs_to_return.append((song["index"], song_title)) 
	else:
		for song in songs:
			song_title = song["title"]
			if song_title.lower().startswith(keywords.lower()):
				songs_to_return.append((song["index"], song_title)) 
	return songs_to_return

def getSongByTitle(userSession, title):
    songBook = userSession.getSongBook()
    index=0
    for song in songBook.get_songs_titles():
        if song.lower() == title.lower():
            return getSongByIndex(userSession, index)
        index+=1
    return None

def getSongByIndex(userSession, song_index):
    if song_index < len(userSession.getSongBook().get_songs_titles()):
        return userSession.getSongBook().get_song_by_index(song_index)
    return None

def getSongByRandom(userSession):
    if userSession.getConfig()["get_random_only_includes_high_tab_scores"] == False:
        return userSession.getSongBook().get_random_song() 
    
    songs =  userSession.getSongBook().get_songs()
    user_activated_layouts= userSession.getHarpLayouts()
    songs_to_select_from = []
    for song in songs:
        if song["source"] == "tabs":
            songs_to_select_from.append(song)
            continue
        if "layout_scores" in song:
            layouts_scores = song["layout_scores"]
            discard = True
            for user_layout in user_activated_layouts:
                user_layout = user_layout.name
                if user_layout in layouts_scores:
                    score = HarpConverter.calcTabScore(layouts_scores[user_layout], userSession.getConfig()["bending"] )
                    if score >= 90.:
                         discard = False
                         break
            if discard:
                continue
            else:
                songs_to_select_from.append(song)
    if len(songs_to_select_from) == 0:
        print("Fallback - No eligable Candidate")
        return userSession.getSongBook().get_random_song() 
    return songs_to_select_from[random.randint(0, len(songs_to_select_from) - 1)]

def querySongs(userSession, query):
    songTitleList = getSongList(userSession, query)
    songs = []
    for songEntry in songTitleList:
        songs.append(getSongByIndex(userSession, songEntry["index"]))
    return songs

def getConfig(userSession):
    return userSession.getConfig()

def saveConfig(userSession, config):
    return userSession.saveConfig(config)

def saveSong(userSession, song):
    userSession.getSongBook().add_song(song)
    userSession.getSongBook().save_songs()

def deleteSong(userSession, song):
    if song["creator"] != userSession.getUserId():
        return False

    userSession.getSongBook().delete_song(song)
    userSession.getSongBook().save_songs()
    return True

def userExists(user_id):
    global userConfigManager
    user_session = HarpTabBotUserSession.HarpTabBotUserSession(user_id, userConfigManager)
    return user_session.load()

def loadSession(user_id):
    global userConfigManager
    user_session = HarpTabBotUserSession.HarpTabBotUserSession(user_id, userConfigManager)
    if not user_session.load():
        user_session.initUser()
    return user_session

def computeTabs(userSession, song):
    layouts = userSession.getHarpLayouts()
    is_bending_proficient = userSession.getConfig()["bending"]
    result_limit = 3
    if userSession.getConfig()["show_best"] == True:
        result_limit = 1
    tabs = HarpConverter.searchBestTabsForSongOverLayouts(song["notes"], layouts, bending=is_bending_proficient, limit=result_limit)
    return tabs

def createSongByABCNotation(userSession, cmd):
    song = NotesImporter.createSongsByABCNotationCom(userSession.getUserId(), cmd)[0]
    return song

def createSongByUserInput(userSession, title, key, notes):
    song = NotesImporter.createSongByUserInput(userSession.getUserId(), title, key, notes)
    return song

def createSongByTabs(userSession, title, tabs):
    song = NotesImporter.createSongByTabs(userSession.getUserId(), title, tabs)
    return song

def localize(user_session, key):
    return localizations[user_session.getLanguage()].get(key)

def recalculateLayoutScores(user_session):
    songs =  user_session.getSongBook().get_songs()
    for song in songs:
        print("Recalculating Layout Scores for {}".format(song["title"]))
        NotesImporter._addLayoutScoreToSong(song)
        user_session.getSongBook().add_song(song)