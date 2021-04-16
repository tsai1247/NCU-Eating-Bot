#!/usr/bin/env python3
# coding=UTF-8
from functions.text_process import preprocess
from functions.interact_with_hackmd import getMenu, getcode, getlist, split
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
            curMenu = getMenu(reply)
            status.pop(chat_id)
            for photolink in curMenu:
                update2.message.reply_photo(photolink)

        elif type==2 and status.get(chat_id)=='random': # random
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
        elif type==3:
            update.callback_query.edit_message_text(reply)
            list = getlist().split('|')
            newlist = []
            for j in range(len(classMap.keys())):
                newlist.append([])
                for i in range((classLen+1)*2+1+j, len(list), len(classMap.keys())+1):
                    if preprocess(list[i])!='':
                        newlist[j].append(list[i].split('[')[1].split(']')[0])
            
            for i in anti_classMap.keys():
                if reply==anti_classMap[i] or reply=='無':
                    list = newlist[i-2]
                    reply = '<b><i>' + anti_classMap[i] + '</i></b>：\n'
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
                    update.message.reply_text(reply, parse_mode=ParseMode.HTML)
        else:
            update.callback_query.edit_message_text('此要求已過期')
        appendlog(getID(update2), update2.message.from_user.full_name, reply)
        