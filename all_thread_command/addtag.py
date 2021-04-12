#!/usr/bin/env python3
# coding=UTF-8
from functions.interact_with_hackmd import get_tags, getshops, update_tag
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading

class thread_addtag(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        chat_id = update.message.chat_id
        try:
            command, shopname, tag = update.message.text.split()
        except ValueError:
            update.message.reply_text('輸入格式為 /addtag 店家 標籤')
            return

        list = getshops()
        if shopname not in list:
            update.message.reply_text('無此店家')
            update.message.reply_text('可先用 /search 查詢正確名稱')
            return
        else:
            tags = get_tags(shopname)
            if tag in tags:
                update.message.reply_text('重複的標籤')
                return
            else:
                update.message.reply_text('正在新增標籤...')
                tags.append(tag)
                update_tag(shopname, tags)
                update.message.reply_text('在{}上新增標籤{}，新增完成。'.format(shopname, tag))

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)