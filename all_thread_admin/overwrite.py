#!/usr/bin/env python3
# coding=UTF-8
# from functions.code_compare import comapreCode
import requests
from functions.checkpermission import checkpermission
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading

class thread_overwrite(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return

        update.message.reply_text('備份中...')

        curMD.push(hackmd=True)
        
        if curMD.text == requests.get('https://hackmd.io/Tz5EFYy-T-Sp9LqpvJkGLg').text.split('<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">')[1].split('</div>')[0]:
            update.message.reply_text('備份成功')
        else:
            update.message.reply_text('備份失敗')
            

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)