#!/usr/bin/env python3
# coding=UTF-8
from interact_with_hackmd import findmenu
from appendlog import appendlog
from dosdefence import getID
from text_process import preprocess
from variable import status, add_query_shopname
import threading


class thread_text(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot

        chat_id = getID(update)
        text = update.message.text
        if chat_id in status:
            state = status[chat_id]
            if state == 'search':
                status.pop(chat_id)
                findmenu(text, update)
            elif state == 'add_step1':
                status.update({chat_id:'add_step2'})
                add_query_shopname.update({chat_id:preprocess(text)})
                update.message.reply_text('新增店家名稱為{}\n請傳送未壓縮照片( /hint ) 或重新輸入名稱'.format(add_query_shopname[chat_id]))
                update.message.reply_text('店家無菜單或傳送完畢請輸入 /add 結束傳送。')
            elif state == 'add_step2':
                add_query_shopname.update({chat_id:preprocess(text)})
                update.message.reply_text('更改店家名稱為{}\n請傳送未壓縮照片( /hint ) 或重新輸入名稱'.format(add_query_shopname[chat_id]))
                update.message.reply_text('店家無菜單或傳送完畢請輸入 /add 結束傳送。')
        else:
            print('ignore it')

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)

            
            