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

class Localization:
    def __init__(self, lang='en', loc_dir='resources/locales'):
        self.lang = lang
        self.loc_dir = loc_dir
        self.translations = self.load_translations()

    def load_translations(self):
        try:
            with open(f'{self.loc_dir}/{self.lang}.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f'Error: Translation file for language "{self.lang}" not found.')
            return {}

    def get(self, key, **kwargs):
        translation = self.translations.get(key, f'[{key}]')
        return translation.format(**kwargs)
