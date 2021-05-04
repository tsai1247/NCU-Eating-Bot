#!/usr/bin/env python3
# coding=UTF-8
from functions.fileRW import read, write
from functions.checkpermission import checkLowerPermission
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading

class thread_delete(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot

        if isDos(update): return
        if(not checkLowerPermission(update)):   return

        update.message.reply_text("菜單刪除功能實作中...")

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
