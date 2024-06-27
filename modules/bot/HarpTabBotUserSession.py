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
from modules.songs import Songs
from modules.engine import HarpLayout
import shutil


class HarpTabBotUserSession:

    def __init__(self, user_id, userConfigManager):
        self.id = user_id
        self.userConfigManager = userConfigManager
        self.callback = None

    def load(self):
        self.config = self.userConfigManager.get_user_config(self.id)
        if self.config == None:
            return False
        self.songbook = Songs.SongManager(song_file="database/songs_{}.json".format(self.config["song_book"]))
        return True

    def initUser(self):
        self.userConfigManager.add_user(self.id )
        self.config = self.userConfigManager.get_user_config(self.id)
        shutil.copyfile("database/songs_default.json", "database/songs_{}.json".format( self.config["song_book"]))
        self.load()

    def getUserId(self):
        return self.id
        
    def getSongBook(self):
        return self.songbook

    def getLanguage(self):
        return self.config["language"]

    def getHarpLayouts(self):
        layouts = []
        for layout_enum in HarpLayout.Harp_Layouts.keys():
            if layout_enum.name in self.config["layouts"]:
                layouts.append(layout_enum)
        return layouts
    
    def getConfig(self):
        return self.config
    
    def saveConfig(self, config):
        self.config = config
        self.userConfigManager.update_user_config(self.id, config)
        self.userConfigManager.save_config()
