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
import json
import random
import os

class SongManager:
    def __init__(self, song_file="database/songs.json"):
        self.SONG_FILE = song_file
        self.SONGS = None
        self.load_songs()

    def sort_songs(self):
        self.SONGS = sorted(self.SONGS, key=lambda x: x['title'].lower())

    def delete_song(self, song):
        self.SONGS.remove(song)

    def load_songs(self):
        if not os.path.exists(self.SONG_FILE):
            self.SONGS =[]
            return
        with open(self.SONG_FILE, "r") as json_file:
            self.SONGS = json.load(json_file)

    def get_songs_titles(self):
        return [entry['title'] for entry in self.SONGS]

    def get_song_by_index(self, index):
        return self.SONGS[index]

    def get_songs(self):
        return self.SONGS

    def get_random_song(self):
        return self.get_song_by_index(random.randint(0, len(self.SONGS) - 1))

    def get_song_by_title(self, title):
        for song in self.SONGS:
            if song["title"] == title:
                return song
        return None

    def add_song(self, song):
        replace_song = None
        for existing_song in self.SONGS:
            if song["title"] == existing_song["title"]:
                replace_song = existing_song
                break
        if replace_song is not None:
            self.SONGS.remove(replace_song)

        self.SONGS.append(song)
        self.sort_songs()
        self.save_songs()

    def save_songs(self):
        with open(self.SONG_FILE, "w") as json_file:
            json.dump(self.SONGS, json_file, indent=4)
