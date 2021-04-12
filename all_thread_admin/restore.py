#!/usr/bin/env python3
# coding=UTF-8
from checkpermission import checkpermission
from overwrite import overwrite
from fileRW import read, Concat_Lines, write
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_restore(threading.Thread):
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
        overwrite('filename_back_up.txt')    
        curData = Concat_Lines(read('filename.txt'))
        write('filename.txt', Concat_Lines(read('filename_back_up.txt')))
        write('filename_auto_back_up.txt', curData)

        update.message.reply_text("以手動備份檔還原完成")

        write('filename.txt', Concat_Lines(read('filename_back_up.txt')))

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)