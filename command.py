#!/usr/bin/env python3
# coding=UTF-8
from thread_add import thread_add
from all_thread_command.thread_clearallrequest import thread_clearallrequest
from fileRW import Concat_Lines
import random
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from interact_with_hackmd import *
from interact_with_imgur import *
from dosdefence import *
from fileRW import *

# TODO: the functions corresponding to each keyword

def start(update, bot):
    if isDos(update): return
    
    update.message.reply_text('Hello.')
    update.message.reply_text('I am just a Eating Bot.')
    help(update, bot)

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def help(update, bot):
    if isDos(update): return
    update.message.reply_text(help_en)
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def helpzh(update, bot):
    if isDos(update): return
    update.message.reply_text(help_zh)
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def randomfunc(update, bot):
    if isDos(update): return

    chat_id = getID(update)
    status.update({chat_id:'random'})
    add_query_update.update({chat_id:update})
    classlist = list(classMap.keys())
    classlist.append('無')
    update.message.reply_text("有什麼要求嗎？",
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 2)) for s in classlist[0::2]],
            [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 2)) for s in classlist[1::2]]
            
        ]))
    
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def add(update, bot):
    thread_add(update).start()

def getClassification(update, bot):
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

def search(update, bot):
    if isDos(update): return
    chat_id = getID(update)
    text = update.message.text.split()

    if len(text) == 1:  # just /search
        status.update({chat_id:'search'})
        update.message.reply_text('請輸入店家名稱')

    else:   # /search with keyword
        keyword = preprocess(Concat_Lines(text[1:]))
        findmenu(keyword, update)

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

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

def filtermsg(update, bot):
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

def DealWithPhotolink(update, file_id):
    chat_id = getID(update)
    if chat_id in status:
        state = status.get(chat_id)
        if state == 'add_step2':
            update.message.reply_text('正在取得照片...')
            photolink = uploadAndGetPhoto(file_id)
            if chat_id in add_query_photolink:  # exist
                add_query_photolink[chat_id].append(photolink)
            else:   # first append
                add_query_photolink[chat_id] = [photolink]
            update.message.reply_text('請繼續傳送照片或輸入 /add 結束傳送')
            append('imagesource.txt', '{}({}): {}, {}\n'.format(chat_id, update.message.from_user.full_name, add_query_shopname.get(chat_id), photolink))
    else:
        print('ignore it')

def whengetphoto(update, bot):
    if isDos(update): return
    update.message.reply_text('為確保資料完整性，請上傳未壓縮照片( /hint )。')
    update.message.reply_text('店家無菜單或傳送完畢請輸入 /add 結束傳送。')
    # DealWithPhotolink(update, update.message.photo[0].file_id)
    appendlog(getID(update), update.message.from_user.full_name, 'getphoto')

def hint(update, bot):
    for i in hint_zh:
        update.message.reply_text(i)

def whengetfile(update, bot):
    if isDos(update): return
    DealWithPhotolink(update, update.message.document.file_id) 
    appendlog(getID(update), update.message.from_user.full_name, 'getfile')

def addtag(update, bot):
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

def clearallrequest(update, bot):
    thread_clearallrequest(update).start()

def listall(update, bot):
    if isDos(update): return

    list = getlist().split('|')
    newlist = []
    for j in range(len(classMap.keys())):
        newlist.append([])
        for i in range((classLen+1)*2+1+j, len(list), len(classMap.keys())+1):
            if preprocess(list[i])!='':
                newlist[j].append(list[i].split('[')[1].split(']')[0])
    
    for i in anti_classMap.keys():
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

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def getID(update):
    return str(update.message.from_user.id)

def report(update, bot):
    if isDos(update): return

    text = update.message.text.split()
    if len(text)==1:
        update.message.reply_text('請使用以下格式回報問題：\n/report 回報內容\n')
        return
    
    name = update.message.from_user.full_name
    chat_type = update.message.chat.type
    text = Concat_Lines(text[1:])        
    append('user_report.txt', '{} as {}: {}\n'.format(name, chat_type, text))
    update.message.reply_text('已將您的問題回報給開發者，感謝您的使用')

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def appendlog(user_id, username, text):
    append('logger.txt', '{}({}): {}\n'.format(user_id, username, text))
