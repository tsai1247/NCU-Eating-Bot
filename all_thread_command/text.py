from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from interact_with_hackmd import Levenshtein, getMenu, getshops
from fileRW import append, read
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading, random

def allin(small, big):
    for c in small:
        if(not c in big):   return False
    return True

def preprocess(text):
    ignorespace = ''
    for i in text:
        if i not in ignore_list:
            ignorespace+=i
    text = ignorespace
    r = read('typo.json')
    for key in r:
        for typo in r[key]:
            text = text.replace(typo, key)

    return text

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

            
            