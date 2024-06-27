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


def bot_show_create_dialogue(bot, user_session, chat):
	keyboard = types.InlineKeyboardMarkup()
	btn_create_by_user_provided_notes = types.InlineKeyboardButton("🎵 {} 🎵".format( HarpTabService.localize(user_session, "add_song_provide_notes")), callback_data="create_notes")
	btn_create_by_user_provided_tabs = types.InlineKeyboardButton("🕳️ {} 🕳️".format( HarpTabService.localize(user_session, "add_song_provide_tabs")), callback_data="create_tabs")
	btn_import_from_abcnotation = types.InlineKeyboardButton("🏠 {} 🏠".format( HarpTabService.localize(user_session, "add_song_abcnotation_import")), callback_data="create_by_abc_import")
	keyboard.add(btn_create_by_user_provided_notes)
	keyboard.add(btn_create_by_user_provided_tabs)
	keyboard.add(btn_import_from_abcnotation)
	bot.send_message(chat.id,  HarpTabService.localize(user_session, "add_song_menu"), reply_markup=keyboard)

def bot_handle_create_control_message(bot, user_session, chat_id, call):
	if "create_tabs" == call.data:
		bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_title"))
		return "create_tabs_title"
	if "create_notes" == call.data:
		bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_title"))
		return "create_notes_title"
	if "create_by_abc_import" == call.data:
		bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_abcnotation_url") )
		return "create_notes_abcnotation"
       

def bot_send_howto_dialogue(bot, chat_id, user_session):
	bot.send_photo(chat_id, photo=open('resources/HowTo_Note_Input.png', 'rb'))
	message = HarpTabService.localize(user_session, "add_song_help")
	message+="\n"
	message+="<pre>"
	message+="A A A A A A | A D F A"+"\n"
	message+="G G G G G G | G C E G"+"\n"
	message+="A A A A A A | A B C2 D2"+"\n"
	message+="C2 A G E | D D"+"\n"
	message+="</pre>"
	bot.send_message(chat_id, message, parse_mode='html')

def bot_callback(bot, user_session, chat_id, callback_command, message):
	if callback_command == "create_tabs_title":
		if message.strip().lower() == "c":
			bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_discarded") )
			return None
		bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_enter_tabs"))
		return "create_tabs_for_{}".format(message.strip())
	elif callback_command.startswith("create_tabs_for_"):
		title = callback_command.split("create_tabs_for_")[1]
		tabs = message
		if tabs.lower().strip() == "c":
			bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_discarded"))
			return None
		song = HarpTabService.createSongByTabs(user_session, title, tabs)
		HarpTabService.saveSong(user_session, song)
		bot.send_message(chat_id,HarpTabService.localize(user_session, "add_song_success").replace("PLACEHOLDER", title))
		return None
	elif callback_command.startswith("create_notes_abcnotation"):
		if message.strip().lower() == "c":
			bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_discarded"))
			return None
		song = HarpTabService.createSongByABCNotation(user_session, message)
		HarpTabService.saveSong(user_session, song)
		bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_abcnotation_success").replace("PLACEHOLDER", song["title"]))
		return None
	if callback_command == "create_notes_title":
		if message.strip().lower() == "c":
			bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_discarded"))
			return None
		bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_enter_notes"))
		return "create_notes_for_{}".format(message.strip())
	elif callback_command.startswith("create_notes_for_"):
		title = callback_command.split("create_notes_for_")[1]
		notes = message
		if notes.lower().strip() == "h":
			bot_send_howto_dialogue(bot, chat_id, user_session)
			bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_enter_notes"))
			return "create_notes_for_{}".format(title)
		if notes.lower().strip() == "c":
			bot.send_message(chat_id, HarpTabService.localize(user_session, "add_song_discarded"))
			return None
		song = HarpTabService.createSongByUserInput(user_session, title, "C", notes)
		HarpTabService.saveSong(user_session, song)
		bot.send_message(chat_id,HarpTabService.localize(user_session, "add_song_success").replace("PLACEHOLDER", title))
		return None