#!/usr/bin/env python3
# coding=UTF-8
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from functions.interact_with_hackmd import Levenshtein, getMenu, getshops
from functions.fileRW import Concat_Lines, append, read
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading, random
from functions.text_process import preprocess, allin

def findmenu(text, update):
    text = preprocess(text)
    chat_id = getID(update)
    list = getshops()
    if text in list:
        curMenu = getMenu(text)
        for photolink in curMenu:
            update.message.reply_photo(photolink)
    else:
        candi_list = []
        print('keyword: {}'.format(text))
        for shop in list:
            if(allin(shop, text) or allin(text, shop) or Levenshtein(shop, text)<2):
                candi_list.append(shop)
        
        if(len(candi_list)>5):
            random.shuffle(candi_list)
            candi_list = candi_list[0:5]

        if(len(candi_list)==0):
            update.message.reply_text('此店家不存在')
            append('non-exist-shop.txt', '{}\n'.format(text))
        else:
            add_query_update.update({chat_id:update})        
            status.update({chat_id:'search_step1'})
            update.message.reply_text("我猜你想查",
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list[0::2]],
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list[1::2]]
                ]))

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)


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
        text = update.message.text.split()

        if len(text) == 1:  # just /search
            status.update({chat_id:'search'})
            update.message.reply_text('請輸入店家名稱')

        else:   # /search with keyword
            keyword = preprocess(Concat_Lines(text[1:]))
            findmenu(keyword, update)

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)