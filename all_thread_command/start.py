#!/usr/bin/env python3
# coding=UTF-8
from all_thread_command.help import thread_help
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading

class thread_start(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        update.message.reply_text('Hello.')
        update.message.reply_text('I am just a Eating Bot.')
        subthread = thread_help(update, self.bot)
        subthread.start()
        subthread.join()


        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
