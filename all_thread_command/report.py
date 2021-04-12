#!/usr/bin/env python3
# coding=UTF-8
from fileRW import Concat_Lines, append
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_report(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return

        text = update.message.text.split()
        if len(text)==1:
            update.message.reply_text('請使用以下格式回報問題：\n/report 回報內容\n')
            return
        
        name = update.message.from_user.full_name
        chat_type = update.message.chat.type
        text = Concat_Lines(text[1:])        
        append('user_report.txt', '{} as {}: {}\n'.format(name, chat_type, text))
        update.message.reply_text('已將您的問題回報給開發者，感謝您的使用')

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)