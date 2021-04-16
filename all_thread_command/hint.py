#!/usr/bin/env python3
# coding=UTF-8
from functions.variable import hint_zh
from telegram import ForceReply
import threading

class thread_hint(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        for i in range(len(hint_zh)):
            if i==len(hint_zh)-1:
                update.message.reply_text(hint_zh[i], reply_markup = ForceReply(selective=True))
            else:
                update.message.reply_text(hint_zh[i])
            