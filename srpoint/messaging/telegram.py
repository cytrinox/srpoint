"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import telepot


class TelegramBot(object):
	def __init__(self, token):
		self.bot_token = token

	def send(self, msg, user):
		bot = telepot.Bot(self.bot_token)
		upd = bot.getUpdates()

		ids = [chat['message']['chat']['id'] for chat in upd if chat['message']['chat']['username'] == user]

		if ids:
			for id in ids:
				bot.sendMessage(id, msg.to_telegram(), parse_mode='markdown')
		else:
			raise Exception("Telegram user {} not found.".format(user))
