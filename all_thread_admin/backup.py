#!/usr/bin/env python3
# coding=UTF-8
from functions.checkpermission import checkpermission
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading

class thread_backup(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return

        update.message.reply_text("備份中...")
        curMD.push(manual=True, hackmd=True)

        update.message.reply_text(
            "手動備份完成"
        )
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
