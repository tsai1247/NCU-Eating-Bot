#!/usr/bin/env python3
# coding=UTF-8
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading

class thread_electric(threading.Thread):
	def __init__(self, update, bot):
		threading.Thread.__init__(self)
		self.update = update
		self.bot = bot
		
	def run(self):
		update = self.update
		bot = self.bot
		
		if isDos(update): return
		
		update.message.reply_text('Bot正常運作中')
		update.message.reply_text('現在顯然有電')
		

		appendlog(getID(update), update.message.from_user.full_name, update.message.text)
