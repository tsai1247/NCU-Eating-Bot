#!/usr/bin/env python3
# coding=UTF-8
from variable import hint_zh
import threading

class thread_hint(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        for i in hint_zh:
            update.message.reply_text(i)