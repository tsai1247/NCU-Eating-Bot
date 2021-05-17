#!/usr/bin/env python3
# coding=UTF-8
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from functions.fileRW import Concat_Lines, append, read
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading, random
from functions.text_process import preprocess, allin
from functions.Levenshtein import Levenshtein
from functions.findmenu import findmenu


class thread_search(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        chat_id = getID(update)

        try:
            command, keyword = update.message.text.split()
            findmenu(keyword, update)
        except:
            status.update({chat_id:'search'})
            update.message.reply_text('請輸入店家名稱', reply_markup = ForceReply(selective=True))

            
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)