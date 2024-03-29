#!/usr/bin/env python3
# coding=UTF-8
from functions.fileRW import read, write
from functions.checkpermission import checkpermission
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading

class thread_addtypo(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot

        if isDos(update): return
        if(not checkpermission(update)):   return

        try:
            correct, wrong = update.message.text[len('/addtypo '):].split()
        except:
            update.message.reply_text('格式錯誤，請使用格式')
            update.message.reply_text('/addtypo 正確詞 錯誤詞')
            return
        r = read("typo.json")
        if correct in r:    r[correct].append(wrong)
        else:   r[correct] = [wrong]
        r = str(r)
        r = r.replace("\'", "\"")
        write("typo.json", r)
        update.message.reply_text("已新增")

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
