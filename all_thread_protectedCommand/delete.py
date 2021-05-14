#!/usr/bin/env python3
# coding=UTF-8
from functions.checkpermission import checkLowerPermission
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import curMD
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

        try:
            command, shopname = update.message.text.split()
        except:
            update.messge.reply_text('格式錯誤，正確格式為：')
            update.messge.reply_text('/delete 店家名稱')
            return
        
        curMD.delete(curMD.getCategory(shopname), shopname, pushNow=True)
        
        update.message.reply_text('店家 {} 已刪除'.format(shopname))

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
