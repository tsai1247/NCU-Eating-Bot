#!/usr/bin/env python3
# coding=UTF-8
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading


class thread_list(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return

        chat_id = getID(update)
        status.update({chat_id:'random'})
        add_query_update.update({chat_id:update})
        classlist = list(classMap.keys())
        classlist.append('無')
        update.message.reply_text("有什麼要求嗎？",
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 3)) for s in classlist[0::2]],
                [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 3)) for s in classlist[1::2]]
                
            ]))


        appendlog(getID(update), update.message.from_user.full_name, update.message.text)