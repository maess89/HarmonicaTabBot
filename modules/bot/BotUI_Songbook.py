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
from telebot import types
from modules.bot import HarpTabService


def bot_show_songbook_dialogue(bot, user_session, chat):
	keyboard = types.InlineKeyboardMarkup()
	btn_default = types.InlineKeyboardButton(HarpTabService.localize(user_session, "songbook_personal"), callback_data="songbook_default")
	btn_global = types.InlineKeyboardButton(HarpTabService.localize(user_session, "songbook_global"), callback_data="songbook_global")
	keyboard.add(btn_default)
	keyboard.add(btn_global)
	bot.send_message(chat.id, HarpTabService.localize(user_session,"songbook_menu"), reply_markup=keyboard)

def bot_handle_songbook_control_message(bot, user_session, chat_id, call):
	user_config = user_session.getConfig()
	the_song_book=call.data.split("songbook_")[1]	
	the_song_book_title = the_song_book
	if the_song_book == "default":
		user_config["song_book"] =user_config["id"]
		the_song_book_title=HarpTabService.localize(user_session, "songbook_personal")
	else:
		user_config["song_book"] =the_song_book

	user_session.saveConfig(user_config)
	user_session.load()
	bot.send_message(chat_id, HarpTabService.localize(user_session, "songbook_success_set").replace("PLACEHOLDER", the_song_book_title))