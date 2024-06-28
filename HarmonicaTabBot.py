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
import telebot
from telebot import types
from telebot import apihelper
from modules.engine import HarpConverter
from modules.engine import HarpLayout
from modules.bot import HarpTabService
from modules.engine import HarpTabUtils
from modules.bot import BotUI_Config
from modules.bot import BotUI_Songbook
from modules.bot import BotUI_CreateSongDialogue
from modules.notes import NotesImporter

BOT_TOKEN="bot.token"

with open(BOT_TOKEN, 'r') as file:
    BOT_TOKEN = file.read()
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


UserSessions={}

def get_commands(user_session):
	return {
		"help": HarpTabService.localize(user_session, 'command_help'),
		"list": HarpTabService.localize(user_session, 'command_list'),
		"get": HarpTabService.localize(user_session, 'command_get'),
		"add": HarpTabService.localize(user_session, 'command_add'),
		"layout": HarpTabService.localize(user_session, 'command_layout'),
		"config": HarpTabService.localize(user_session, 'command_config'),
		"delete": HarpTabService.localize(user_session, 'command_delete'),
		"dump": HarpTabService.localize(user_session, 'command_dump'),
# TODO: Removed Song Book Feature
#		"songbook": HarpTabService.localize(user_session, 'command_songbook'),
		"howto": HarpTabService.localize(user_session, 'command_howto')
	}

def init_commands(user_session, chat_id):
	commands_dict=get_commands(user_session)
	commands = []
	for command_key in commands_dict.keys():
		commands.append(types.BotCommand(command=command_key, description=commands_dict[command_key]))
	bot.set_my_commands(commands,  scope=telebot.types.BotCommandScopeChat(chat_id))


CHAT_CALLBACKS = {}
def getChatCallback(user_id):
	if user_id in CHAT_CALLBACKS:
		return CHAT_CALLBACKS[user_id]
	return None

def setChatCallback(user_id, callback_command):
	CHAT_CALLBACKS[user_id] = callback_command

def load_or_create_session(chat_id):
	global UserSessions
	user_id=str(chat_id)
	if user_id not in UserSessions:
		UserSessions[chat_id] = HarpTabService.loadSession(user_id)
	user_session = UserSessions[chat_id]
	return user_session

def get_song_by_user_input(user_session, cmd, getRandomOnEmpty=True):
	cmd = cmd.strip()
	if cmd.startswith("/"):
		cmd = cmd[1:]
	cmd_parts = cmd.split(" ")
	song = None
	if len(cmd_parts[0]) == 0 and getRandomOnEmpty:
		song=HarpTabService.getSongByRandom(user_session)
	else:
		if cmd_parts[0].isdigit():
			index = int(cmd_parts[0])-1
			song = HarpTabService.getSongByIndex(user_session, index)
		else:
			song_title = ' '.join(cmd_parts)
			song = HarpTabService.getSongByTitle(user_session, song_title)
	return song

def delete_song(chat, user_session, song):
	success = HarpTabService.deleteSong(user_session, song)
	if success:
		bot.send_message(chat.id, HarpTabService.localize(user_session, 'confirmed_song_deleted').replace("PLACEHOLDER", song["title"]))
	else:
		bot.send_message(chat.id, HarpTabService.localize(user_session, 'rejected_song_deleted').replace("PLACEHOLDER", song["title"]))
def convert_and_send_song(chat, user_session, song):
	if song["source"] == "tabs":
		message="<b>{}</b>\n".format(song["title"])
		message+="<i>"+"Tabs"+"</i>"
		message+="\n"
		message+="<pre>"
		message+=song["tabs"]
		message+="</pre>"
		bot.send_message(chat.id, message, parse_mode='html')
		return

	tabs = HarpTabService.computeTabs(user_session, song)
	for tab in tabs:
		message="<b>{}</b>\n".format(song["title"])
		layout_and_score="{} (Score: {}%)".format(HarpTabService.localize(user_session, tab["harp_layout"]["name"]), round(HarpConverter.calcTabScore(tab["stats"], user_session.getConfig()["bending"] ),0))
		message+="<i>"+layout_and_score+"</i>"
		message+="\n"
		message+="<pre>"
		message+=HarpTabUtils.convert_harp_tabs_to_beautiful_string(tab["tabs"])
		message+="</pre>"
		bot.send_message(chat.id, message, parse_mode='html')

def send_howto_convert_message(chat, user_session):
	message= HarpTabService.localize(user_session, "howto_title")
	bot.send_message(chat.id, message)
	BotUI_CreateSongDialogue.bot_send_howto_dialogue(bot, chat.id, user_session)

def bot_show_song_list(user_session, chat, filter=None):
	songs = HarpTabService.getSongList(user_session)
	return_message = "{}\n\n".format(HarpTabService.localize(user_session, 'list_of_your_songs'))
	for song in songs:
		return_message+="\t/{}. {}\n".format(song["index"]+1, song["title"])
	bot.send_message(chat.id, return_message)

def bot_show_song_list_and_filter_by_string(chat, user_session, cmd):
	songs = HarpTabService.getSongList(user_session, keywords=cmd)
	if len(songs) == 0:
		bot.send_message(chat.id, "{}".format(HarpTabService.localize(user_session, 'could_not_find_song_message')))
		return

	return_message = "{}\n\n".format(HarpTabService.localize(user_session, 'list_of_your_songs'))
	for song in songs:
		return_message+="\t/{}. {}\n".format(song["index"]+1, song["title"])
	bot.send_message(chat.id, return_message)

def bot_dump_song(bot, chat, song):
	message="<b>Title</b>: <i>{}</i>".format(song["title"])+"\n\n"
	if "notes" in song:
		message+="<b>Notes</b>:\n<pre>{}</pre>".format(HarpTabUtils.convert_song_to_readable_array(song["notes"]))+"\n\n"
	elif "tabs" in song:
		message+="<b>Tabs</b>:\n<pre>{}</pre>".format(song["tabs"])+"\n\n"
	if "creator" in song:
		message+="<b>Creator</b>: {}".format(song["creator"])+"\n\n"
	if "date" in song:
		message+="<b>Date</b>: {}".format(song["date"])+"\n\n"
	if "source" in song:
		message+="<b>Source</b>: {}".format(song["source"])+"\n\n"
	if "url" in song:
		message+="<b>URL</b>: {}".format(song["url"])+"\n\n"
	if "raw" in song:
		message+="<b>Raw User Input</b>:\n<pre>{}</pre>".format(song["raw"])+"\n\n"
	if "layout_scores" in song:
		message+="<b>Layout Tab Scores:</b>"+"\n"
		layouts = HarpLayout.Harp_Layouts
		for layout in layouts:
			if layout.name in song["layout_scores"]:
				layout_score_string = round(HarpConverter.calcTabScore(song["layout_scores"][layout.name], False ),0)
				message+="   - {}: {}%\n".format(layout._name_, layout_score_string)
	bot.send_message(chat.id, message, parse_mode='html')


def _user_input_is_command(user_input, cmdPatterns):
	for cmdPattern in cmdPatterns:
		if user_input.lower().startswith(cmdPattern.lower()):
			return True
	return False

def _user_input_get_command_args(user_input, cmdPatterns):
	for cmdPattern in cmdPatterns:
		if user_input.startswith(cmdPattern):
			return user_input.replace(cmdPattern, "")
	return user_input

def bot_convert_song_notes_on_the_fly(user_session, chat, cmd):
	notes = NotesImporter.createSongByUserInput(user_session.getUserId(), HarpTabService.localize(user_session, "your_song"), "C", cmd)
	parsed_notes = notes["notes"]
	if len(parsed_notes) > 0:
		total_tokens = len(notes["notes"])
		symbol_cnt = 0
		for note in parsed_notes:
			if isinstance(note, list):
				symbol_cnt+=1
		note_cnt = total_tokens - symbol_cnt
		if note_cnt > 2 and (note_cnt/float(total_tokens) > 0.3):
			convert_and_send_song(chat, user_session, notes)
			return True
	return False

def handle_cmd(user_session, chat, cmd):
	if getChatCallback(user_session.getUserId()) is not None:
		callback_command = getChatCallback(user_session.getUserId())
		setChatCallback(user_session.getUserId(), None)
		callback_command = BotUI_CreateSongDialogue.bot_callback(bot, user_session, chat.id, callback_command, cmd)
		setChatCallback(user_session.getUserId(), callback_command)
		return
	elif _user_input_is_command(cmd, ["/help", "help", "/start", "start"]):
		send_welcome_message(chat.id, user_session)
		return
	elif _user_input_is_command(cmd, ["/songbook", "songbook"]):
		BotUI_Songbook.bot_show_songbook_dialogue(bot, user_session, chat)
	elif _user_input_is_command(cmd, ["/list", "list", "ls"]):
		bot_show_song_list(user_session, chat)
	elif _user_input_is_command(cmd, ["/dump", "dump"]):
		song = get_song_by_user_input(user_session, _user_input_get_command_args(cmd, ["/dump", "dump"]))
		if song == None:
			bot.send_message(chat.id, HarpTabService.localize(user_session, 'could_not_find_song_message'))
			return
		bot_dump_song(bot, chat, song)
	elif _user_input_is_command(cmd, ["/get", "get"]):
		song = get_song_by_user_input(user_session, _user_input_get_command_args(cmd, ["/get", "get"]))
		if song == None:
			bot.send_message(chat.id, "{}".format(HarpTabService.localize(user_session, 'could_not_find_song_message')))
			return
		convert_and_send_song(chat, user_session, song)
	elif _user_input_is_command(cmd, ["/delete", "delete"]):
		song = get_song_by_user_input(user_session, _user_input_get_command_args(cmd, ["/delete", "delete"]), getRandomOnEmpty=False)
		if song == None:
			bot.send_message(chat.id, HarpTabService.localize(user_session, 'could_not_find_song_message'))
			return
		delete_song(chat, user_session, song)
	elif _user_input_is_command(cmd, ["/add", "add"]):
		BotUI_CreateSongDialogue.bot_show_create_dialogue(bot, user_session, chat)
	elif _user_input_is_command(cmd, ["/config", "config"]):
		BotUI_Config.bot_show_config_dialogue(bot, user_session, chat)
	elif _user_input_is_command(cmd, ["/layout", "layout"]):
		BotUI_Config.bot_show_layout_dialogue(bot, user_session, chat)
	elif _user_input_is_command(cmd, ["/howto", "howto"]):
		send_howto_convert_message(chat, user_session)
	else:
		song = get_song_by_user_input(user_session, cmd)
		if song is not None:
			convert_and_send_song(chat, user_session, song)
		else:
			# Parse User Input for instant conversion feature
			success = bot_convert_song_notes_on_the_fly(user_session, chat, cmd)
			if not success:
				bot_show_song_list_and_filter_by_string(chat, user_session, cmd)

def send_welcome_message(chat_id, user_session):
	commands = get_commands(user_session)
	message = HarpTabService.localize(user_session, 'welcome_message')
	message +="\n"
	message +="\n"
	message +=HarpTabService.localize(user_session, 'welcome_message_body')
	message +="\n"

	# TODO: Removed Song Book Feature
	#settings = ["layout", "config", "songbook"]
	settings = ["layout", "config"]
	message +="\n{}:".format(HarpTabService.localize(user_session, 'welcome_settings'))
	message +="\n"
	for command_key in settings:
		message+="\t o /{} - {}".format(command_key, commands[command_key])
		message+="\n"

	song_ops = ["list", "get", "add", "delete", "dump"]
	message +="\n{}:".format(HarpTabService.localize(user_session, 'welcome_functions'))
	message +="\n"
	for command_key in song_ops:
		message+="\t o /{} - {}".format(command_key, commands[command_key])
		message+="\n"

	song_ops = ["help", "howto"]
	message +="\n{}:".format(HarpTabService.localize(user_session, 'welcome_help'))
	message +="\n"
	for command_key in song_ops:
		message+="\t o /{} - {}".format(command_key, commands[command_key])
		message+="\n"

	bot.send_message(chat_id, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
	chat_id=call.message.chat.id
	user_session = load_or_create_session(chat_id)
	if call.data.startswith("config_"):
		BotUI_Config.bot_handle_config_control_message(bot, user_session, chat_id, call)
	elif  call.data.startswith("songbook_"):
		BotUI_Songbook.bot_handle_songbook_control_message(bot, user_session, chat_id, call)
	elif call.data.startswith("create_"):
		callback_return = BotUI_CreateSongDialogue.bot_handle_create_control_message(bot, user_session, chat_id, call)
		setChatCallback(user_session.getUserId(), callback_return)

@bot.message_handler(func=lambda m: True)
def response_bot(message):
	chat_id= message.chat.id
	user_exists = HarpTabService.userExists(chat_id)
	user_session = load_or_create_session(chat_id)
	init_commands(user_session, chat_id)
	if not user_exists:
		send_welcome_message(chat_id, user_session)
		return

	bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands('commands'))
	handle_cmd(user_session, message.chat, message.text)
	return

bot.infinity_polling()
