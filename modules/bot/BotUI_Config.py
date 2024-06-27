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
from telebot import apihelper
from modules.engine import HarpLayout
from modules.bot import HarpTabService

def _get_layout_configuration_keyboard(user_session):
	keyboard = types.InlineKeyboardMarkup()
	for layout in HarpLayout.Layout:
		verb="❌"
		if layout in user_session.getHarpLayouts():
			verb="✅"
		layout_dict = HarpLayout.Harp_Layouts[layout]
		layout_name = layout_dict["name"]
		description="{} {}".format(HarpTabService.localize(user_session, layout_name), verb)
		btn_layout = types.InlineKeyboardButton(description, callback_data="config_layout_"+layout_dict["layout"].name)
		keyboard.add(btn_layout)

	btn_close = types.InlineKeyboardButton("- {} -".format(HarpTabService.localize(user_session, "config_close")), callback_data="config_close")
	keyboard.add(btn_close)

	return keyboard

def _get_layout_configuration_more(user_session, config):
	keyboard = types.InlineKeyboardMarkup()

	language_flag_to = "🇬🇧"
	if user_session.getLanguage() == 'en':
		language_flag_to = "🇩🇪"
	
	btn_language = types.InlineKeyboardButton("{}".format(HarpTabService.localize(user_session, "config_language").replace("PLACEHOLDER", language_flag_to)), callback_data="config_language")
	keyboard.add(btn_language)

	verb="❌"
	if config["bending"] == True:
		verb="✅"
	btn_bending = types.InlineKeyboardButton("{} {}".format(HarpTabService.localize(user_session, "config_bending"), verb), callback_data="config_custom_bending")
	keyboard.add(btn_bending)

	verb="❌"
	if config["show_best"] == True:
		verb="✅"
	btn_show_best = types.InlineKeyboardButton("{} {}".format(HarpTabService.localize(user_session, "config_show_best_only"), verb), callback_data="config_custom_show_best")
	keyboard.add(btn_show_best)

	verb="❌"
	if config["get_random_only_includes_high_tab_scores"] == True:
		verb="✅"
	btn_show_best = types.InlineKeyboardButton("{} {}".format(HarpTabService.localize(user_session, "config_get_random_only_includes_high_tab_scores"), verb), callback_data="config_get_random_only_high_tab_score")
	keyboard.add(btn_show_best)

	btn_close = types.InlineKeyboardButton("- {} -".format(HarpTabService.localize(user_session, "config_close")), callback_data="config_close")
	keyboard.add(btn_close)

	return keyboard

def _bot_edit(bot, chat_id, text, message_id, reply_markup):
	try:
		bot.edit_message_text(chat_id=chat_id, text=text, message_id=message_id, reply_markup=reply_markup)
	except apihelper.ApiTelegramException:
		pass

def bot_show_layout_dialogue(bot, user_session, chat):
	bot.send_message(chat.id, HarpTabService.localize(user_session, "config_layout"), reply_markup=_get_layout_configuration_keyboard(user_session))

def bot_show_config_dialogue(bot, user_session, chat):
	bot.send_message(chat.id, HarpTabService.localize(user_session, "config_more_settings"), reply_markup=_get_layout_configuration_more(user_session, user_session.getConfig()))


def bot_handle_config_control_message(bot, user_session, chat_id, call):
	user_config= user_session.getConfig()
	if "config_main" in call.data:
		_bot_edit(bot, chat_id, text=HarpTabService.localize(user_session, "config_layout"), message_id=call.message.id, reply_markup=_get_layout_configuration_keyboard(user_session))
	elif "config_layout_more" in call.data:
		_bot_edit(bot, chat_id, text=HarpTabService.localize(user_session, "config_more_settings"), message_id=call.message.id, reply_markup=_get_layout_configuration_more(user_session, user_config))
	elif "config_layout_" in call.data:
		selected_layout = call.data.replace("config_layout_", "")
		if selected_layout in user_session.getConfig()["layouts"]:
			user_config["layouts"].remove(selected_layout)
		else:
			user_config["layouts"].append(selected_layout)
		user_session.saveConfig(user_config)
		_bot_edit(bot, chat_id, text=HarpTabService.localize(user_session, "config_layout"), message_id=call.message.id, reply_markup=_get_layout_configuration_keyboard(user_session))
	elif "config_custom_show_best" in call.data:
		user_config["show_best"] = not user_config["show_best"]
		user_session.saveConfig(user_config)
		call.data="config_layout_more"
		return bot_handle_config_control_message(bot, user_session, chat_id, call)
	elif "config_custom_bending" in call.data:
		user_config["bending"] = not user_config["bending"]
		user_session.saveConfig(user_config)
		call.data="config_layout_more"
		return bot_handle_config_control_message(bot, user_session, chat_id, call)
	elif "config_get_random_only_high_tab_score" in call.data:
		user_config["get_random_only_includes_high_tab_scores"] = not user_config["get_random_only_includes_high_tab_scores"]
		user_session.saveConfig(user_config)
		call.data="config_layout_more"
		return bot_handle_config_control_message(bot, user_session, chat_id, call)
	elif "config_language" in call.data:
		next_language = user_config["language"]
		if next_language == "en":
			next_language = "de"
		else:
			next_language = "en"
		user_config["language"] = next_language
		user_session.saveConfig(user_config)
		_bot_edit(bot, chat_id, text=HarpTabService.localize(user_session, "config_more_settings"), message_id=call.message.id, reply_markup=_get_layout_configuration_more(user_session, user_config))
	elif "config_position_" in call.data:
		selected_position = call.data.replace("config_position_", "")
		user_config["positions"][selected_position]=not user_config["positions"][selected_position]
		user_session.saveConfig(user_config)
		call.data="config_layout_more"
		return bot_handle_config_control_message(bot, user_session, chat_id, call)
	elif "config_close" in call.data:
		try:
			bot.delete_message(chat_id=chat_id, message_id=call.message.id)
		except apihelper.ApiTelegramException:
			pass