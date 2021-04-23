#!/usr/bin/env python3
# coding=UTF-8
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from functions.appendlog import appendlog
from functions.interact_with_hackmd import updateHackmd
from functions.interact_with_imgur import getNoMenuLink
from functions.dosdefence import getID, isDos
from functions.variable import *
import threading

class thread_add(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        
        chat_id = getID(update)
        while status.get(chat_id) == "photo_update":
            add_query_photo_lock.get(chat_id).acquire()
            add_query_photo_lock.get(chat_id).release()

        if status.get(chat_id) == "add_step2":
            status.pop(chat_id)
            update.message.reply_text('正在新增店家...')
            cur_classification = add_query_classification.get(chat_id)
            cur_shopname = add_query_shopname.get(chat_id)
            if(chat_id in add_query_photolink):
                cur_photolink = add_query_photolink.get(chat_id)
            else:
                cur_photolink = [getNoMenuLink()]
            updateHackmd(chat_id, cur_classification, cur_shopname, cur_photolink)
            update.message.reply_text('新增店家 {} 於分類 {}, 新增完成。'.format(cur_shopname, cur_classification))
        else:
            add_query_update.update({chat_id:update})
            status.update({chat_id:'add_step0'})
            update.message.reply_text("請選擇分類",
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 0)) for s in list(classMap.keys())[0::2]],
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 0)) for s in list(classMap.keys())[1::2]]
                ]))

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
