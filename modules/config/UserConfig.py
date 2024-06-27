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
import threading
from modules.engine import HarpLayout

class UserConfigManager:
    def __init__(self, config_file="user_config.json"):
        self.config_file = config_file
        self.lock = threading.Lock()
        self.user_config = self.load_config()

    def load_config(self):
        with open(self.config_file, "r") as json_file:
            return json.load(json_file)

    def save_config(self):
        with open(self.config_file, "w") as json_file:
            json.dump(self.user_config, json_file, indent=4)

    def has_user(self, user_id):
        return self.get_user_config(user_id) is not None

    def add_user(self, user_id):
        user_id =str(user_id)
        with self.lock:
            self.user_config[user_id] = {
                "id": user_id,
                "layouts": [
                   HarpLayout.Layout.Major_Diatonic.name
                ],
                "bending": False,
                "get_random_only_includes_high_tab_scores": True,
                "show_best": True,
                "song_book": user_id,
                "language": "en"
            }
            self.save_config()

    def get_user_config(self, user_id):
        user_id= str(user_id)
        with self.lock:
            if user_id in self.user_config:
                return self.user_config[user_id]
        return None


    def update_user_config(self, user_id, config):
        user_id=str(user_id)
        with self.lock:
            if user_id in self.user_config:
                self.user_config[user_id] = config
                self.save_config()
            else:
                print("User ID {} not found.".format(user_id))
