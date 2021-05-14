#!/usr/bin/env python3
# coding=UTF-8
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
from functions.variable import curMD
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
            
        tag = '`' + tag + '`'
        list = curMD.getshops()
        Done = False
        for i in list:
            if shopname in i:
                Done = True
                tags = curMD.getTag(shopname)
                print(tags)
                if tag in tags:
                    update.message.reply_text('重複的標籤')
                else:
                    update.message.reply_text('正在新增標籤...')
                    tags.append(tag)
                    curMD.editTag(shopname, tags)
                    update.message.reply_text('在{}上新增標籤{}，新增完成。'.format(shopname, tag))
                break
        if not Done:
            update.message.reply_text('無此店家')
            update.message.reply_text('可先用 /search 查詢正確名稱')
        
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)