#!/usr/bin/env python3
# coding=UTF-8
from functions.fileRW import Concat_Lines, read, write
from functions.overwrite import overwrite
from functions.checkpermission import checkpermission
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading

class thread_undo(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return

        update.message.reply_text("還原中...")
        overwrite('filename_auto_back_up.txt')
        curData = Concat_Lines(read('filename.txt'))
        write('filename.txt', Concat_Lines(read('filename_auto_back_up.txt')))
        write('filename_auto_back_up.txt', curData)

        update.message.reply_text("以自動備份檔還原完成")

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
