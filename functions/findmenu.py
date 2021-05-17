from functions.text_process import preprocess, allin
from functions.dosdefence import getID
from functions.variable import curMD, add_query_update, status
from functions.Levenshtein import Levenshtein
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from functions.fileRW import append

def findmenu(text, update):
    text = preprocess(text)
    chat_id = getID(update)
    list = curMD.getshops()

    newlist = []
    for i in list:
        newlist+=i

    list = newlist

    if text in list:
        curMenu = curMD.getMenu(text)
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
            print('candicate:', candi_list)
            add_query_update.update({chat_id:update})        
            status.update({chat_id:'search_step1'})
            update.message.reply_text("我猜你想查",
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list[0::2]],
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list[1::2]]
                ]))