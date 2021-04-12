#!/usr/bin/env python3
# coding=UTF-8
from interact_with_hackmd import getMenu, getcode, split
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading, random

class thread_callback(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot

        reply, chat_id, type = update.callback_query.data.split(" ")
        update2 = ''
        if chat_id in add_query_update:
            update2 = add_query_update.get(chat_id)
            add_query_update.pop(chat_id)
        else:
            update.callback_query.edit_message_text('此要求已過期')
            return
        type = int(type)

        if type == 0 and status.get(chat_id)=='add_step0':  # add
            update.callback_query.edit_message_text('分類為：{}\n請輸入店家名稱'.format(reply))
            
            status.update({chat_id:'add_step1'})
            add_query_classification[chat_id] = reply

        elif int(type)==1 and status.get(chat_id)=='search_step1': # search
            update.callback_query.edit_message_text(reply)
            curMenu = getMenu(reply)
            status.pop(chat_id)
            for photolink in curMenu:
                update2.message.reply_photo(photolink)

        elif int(type)==2 and status.get(chat_id)=='random': # random
            def random_menu(code, s):
                if s=='無':
                    pass
                else:
                    code = split(getcode())[classMap[s]]
                rd = code.split('###')
                if(len(rd)-1<1):
                    return ""
                ret = rd[random.randint(1, len(rd)-1)].split('###')[0]
                return ret

            def sort(rand_shop):
                if(rand_shop==""):
                    return ""
                cur = rand_shop.split('![]')
                for i in range(1, len(cur)):
                    cur[i] = cur[i].split('(')[1].split(' =400x')[0]
                return cur

            def push_menu(sorted_shop):
                if(sorted_shop==""):
                    update2.message.reply_text('此分類暫時無店家')
                update2.message.reply_text(sorted_shop[0])
                for i in range(1, len(sorted_shop)):
                    update2.message.reply_photo(sorted_shop[i])
            
            status.pop(chat_id)
            update.callback_query.edit_message_text('條件： {}'.format(reply))
            push_menu(sort(random_menu(getcode(), reply)))
        else:
            update.callback_query.edit_message_text('此要求已過期')
        appendlog(getID(update2), update2.message.from_user.full_name, reply)
        