#!/usr/bin/env python3
# coding=UTF-8
from functions.appendlog import appendlog
from functions.dosdefence import getID
from functions.variable import *
from telegram import ForceReply, ParseMode
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
            update.callback_query.edit_message_text('分類為：{}\n'.format(reply))
            update2.message.reply_text('請輸入店家名稱', reply_markup = ForceReply(selective=True))
            
            status.update({chat_id:'add_step1'})
            add_query_classification[chat_id] = reply

        elif type==1 and status.get(chat_id)=='search_step1': # search
            update.callback_query.edit_message_text(reply)
            curMenu = curMD.getMenu(reply)
            status.pop(chat_id)
            for photolink in curMenu:
                update2.message.reply_photo(photolink)

        elif type==2 and status.get(chat_id)=='random': # random
            def random_shop(category):
                if category == '無':
                    list = []
                    for i in curMD.getshops():
                        list += i
                else:
                    list = curMD.getshops()[classMap[category]-2]
                
                random.shuffle(list)
                if list == []:
                    return None
                else:
                    return list[0]

            def push_menu(curShop, curMenu):
                if(curMenu==[]):
                    update2.message.reply_text('此分類暫時無店家')
                    return
                update2.message.reply_text(curShop)
                for link in curMenu:
                    update2.message.reply_photo(link)
            
            status.pop(chat_id)
            update.callback_query.edit_message_text('條件： {}'.format(reply))
            curShop = random_shop(reply)
            push_menu(curShop, curMD.getMenu(curShop))

        elif type==3: #list
            update.callback_query.edit_message_text(reply)  # reply is the category
            user_reply = reply

            if user_reply =='無':
                list = []
                for i in curMD.getshops():
                    list += i
            else:
                list = curMD.getshops()[classMap[user_reply]-2]

            reply = ''
            
            count = 0
            max_word = 4
            single_line_cnt = 3
            
            for shop in list:
                reply += shop
                count += 1
                if count%single_line_cnt==0:
                    reply+='\n'
                elif len(shop)>max_word:
                    reply+='\n'
                    count = 0
                else:
                    for j in range(max_word-len(shop)+1):
                        reply += '\t\t\t\t'
            if reply =='':
                reply = '此分類暫時無店家'
            update2.message.reply_text(reply, parse_mode=ParseMode.HTML)

        else:
            update.callback_query.edit_message_text('此要求已過期')
        appendlog(getID(update2), update2.message.from_user.full_name, reply)
        