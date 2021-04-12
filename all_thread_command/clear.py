#!/usr/bin/env python3
# coding=UTF-8
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading


class thread_clear(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot

        if isDos(update): return

        chat_id = getID(update)
        if chat_id in status:
            status.pop(chat_id)
        if chat_id in add_query_shopname:
            add_query_shopname.pop(chat_id)
        if chat_id in add_query_classification:
            add_query_classification.pop(chat_id)
        if chat_id in add_query_photolink:
            add_query_photolink.pop(chat_id)
        if chat_id in add_query_update:
            add_query_update.pop(chat_id)
        update.message.reply_text("已清除您的所有要求")

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
