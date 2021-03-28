#!/usr/bin/env python3
# coding=UTF-8
from os import stat
import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from interact_with_hackmd import *
from interact_with_imgur import *
from dosdefence import *

# TODO: the functions corresponding to each keyword

def start(update, bot):
    if isDos(update): return
    update.message.reply_text(
        'Hello.'
    )
    update.message.reply_text(
        'I am just a Eating Bot.'
    )
    help(update, bot)
    # bot.send_photo(
    #     chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def help(update, bot):
    if isDos(update): return
    update.message.reply_text(
        'The followings are some commands: \n'
        '/helpzh : 查看中文說明\n'
        '/help : get this document.\n'
        '/random : get a random restaurant menu.\n'
        '/search : search a menu.\n'
        '/add : add new menu.\n'
        '/list : list all menu.\n'
        '/addtag : add tag for a shop.\n'
        '/report: report the bot\'s problems\n'
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def help_zh(update, bot):
    if isDos(update): return
    update.message.reply_text(
        '以下是常用的指令: \n'
        '/help : English document\n'
        '/helpzh : 查看此說明。\n'
        '/random : 隨機取得一個菜單。\n'
        '/search : 查詢菜單。\n'
        '/add : 新增菜單。\n'
        '/list : 列出所有店家。\n'
        '/addtag : 在店家上新增標籤。\n'
        '/report: 回報Bot的問題。\n'
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def randomfunc(update, bot):
    if isDos(update): return

    chat_id = getID(update)
    if(chat_id in status):
        del(status[chat_id])
    status[chat_id] = 'random'
    if(chat_id in add_query_update):
        del(add_query_update[chat_id])
    add_query_update[chat_id] = update
    update.message.reply_text("有什麼要求嗎？",
            reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 2)) for s in ['宵夜街', '後門', '奢侈街', '山下', '無']
                ]]))
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def add(update, bot):
    if isDos(update): return
    chat_id = getID(update)
    # status[chat_id] = "add_step1"

    # update.message.reply_text(
    #     '請輸入店家名稱'
    # )
    try:
        if status[chat_id] == "add_step2":
            del(status[chat_id])
            update.message.reply_text(
                    '正在新增店家...'
                )
            cur_classification = add_query_classification[chat_id]
            cur_shopname = add_query_shopname[chat_id]
            cur_photolink = add_query_photolink[chat_id]
            
            updateHackmd(chat_id, cur_classification, cur_shopname, cur_photolink)
            update.message.reply_text(
                '新增店家 {} 於分類 {}, 新增完成。'.format(cur_shopname, cur_classification)
            )

    except KeyError:
        if(chat_id in add_query_update):
           del(add_query_update[chat_id])
        add_query_update[chat_id] = update
        update.message.reply_text("請選擇分類",
            reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 0)) for s in ['宵夜街', '後門', '奢侈街', '山下']
                ]]))
    print('status:', status)
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def getClassification(update, bot):
    s, chat_id, type = update.callback_query.data.split(" ")
    if(chat_id in add_query_update):
        update2 = add_query_update[chat_id]
        del(add_query_update[chat_id])
    if int(type)==0 :
        update.callback_query.edit_message_text(
            '分類為：{}\n請輸入店家名稱'.format(s)
        )
        if chat_id in status:
            del(status[chat_id])
        status[chat_id] = "add_step1"
        add_query_classification[chat_id] = s
        print('status:', status)
    elif int(type)==1 :
        curMenu = getMenu(s)
        #### TODO:
        update.callback_query.edit_message_text(
            s
        )
        for i in curMenu:
            update2.message.reply_photo(
                i
            )
    elif int(type)==2 :
        def random_menu(code, s):
            if s=='無':
                pass
            else:
                code2 = split(getcode())
                location = classMap[s]
                code = code2[location]

            rd = code.split('###')
            ret = rd[random.randint(1, len(rd)-1)].split('###')[0]
            return ret
        def sort(rand_shop):
            cur = rand_shop.split('![]')
            for i in range(1, len(cur)):
                cur[i] = cur[i].split('(')[1].split(' =400x')[0]
            return cur
        def push_menu(sorted_shop):
            update2.message.reply_text(
                sorted_shop[0]
            )
            for i in range(1, len(sorted_shop)):
                update2.message.reply_photo(
                    sorted_shop[i]
                )
        if chat_id in status:
            del(status[chat_id])

        update.callback_query.edit_message_text(
                '條件： ' + s
        )
        push_menu(
            sort(
                random_menu(
                    getcode(), s
        )))
    appendlog(getID(update2), update2.message.from_user.full_name, s)
def search(update, bot):
    if isDos(update): return
    chat_id = getID(update)
    ori_text = update.message.text
    if(len(ori_text)<=len('/search ')):
        if(chat_id in status):
            del(status[chat_id])
        status[chat_id] = "search"
        update.message.reply_text(
            '請輸入店家名稱'
        )
    else:
        text = ori_text[len('/search'):]
        findmenu(text, update)
    print('status:', status)
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def allin(small, big):
    for i in small:
        if(not i in big):
            return False
    return True

def preprocess(text):
    ignorespace = ''
    for i in text:
        if(i!=' ' and i != '\n'):
            ignorespace+=i
    text = ignorespace
    fp = codecs.open("typo.json", "r", "utf-8")
    r = json.load(fp)
    fp.close()

    for key in r:
        for typo in r[key]:
            while(typo in text):
                index = text.index(typo)
                lens = len(typo)
                text = text[0:index] + key + text[(index+lens):]
    return text

def findmenu(text, update):
    text = preprocess(text)
    chat_id = getID(update)
    list = getshops()
    if text in list:
        curMenu = getMenu(text)
        for i in curMenu:
            update.message.reply_photo(
                i
            )
    else:
        candi_list = []
        print('keyword: {}'.format(text))
        for shop in list:
            if(allin(shop, text) or allin(text, shop)):
                candi_list.append(shop)
            elif(Levenshtein(shop, text)<2):
                candi_list.append(shop)

        if('名豐' in text and ('請客' in text or 'treat' in text or 'おご' in text ) and (text.count('不')+text.count('treated') + text.count('被') + text.count('れた') + text.count('no')+text.count('ない'))%2==0):
            candi_list = list
        
        if(len(candi_list)>5):
            random.shuffle(candi_list)
            candi_list = candi_list[0:5]

        if(len(candi_list)==0):
            update.message.reply_text(
                '此店家不存在'
            )
            fp = codecs.open("non-exist-shop.txt", "a", "utf-8")
            fp.write(text + '\n')
            fp.close()
        else:
            if(chat_id in add_query_update):
                del(add_query_update[chat_id])
            add_query_update[chat_id] = update
            update.message.reply_text("我猜你想查",
                reply_markup = InlineKeyboardMarkup([[
                        InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list
                ]]))

def filtermsg(update, bot):
    chat_id = getID(update)
    text = update.message.text
    try:
        state = status[chat_id]
        if state == 'search':
            del(status[chat_id])
            findmenu(text, update)

        elif state == 'add_step1':
            del(status[chat_id])
            status[chat_id] = "add_step2"
            add_query_shopname[chat_id] = preprocess(text)
            update.message.reply_text(
                '新增店家名稱為{}\n請傳送照片或重新輸入名稱'.format(add_query_shopname[chat_id])
            )
        elif state == 'add_step2':
            del(status[chat_id])
            status[chat_id] = "add_step2"
            del(add_query_shopname[chat_id])
            add_query_shopname[chat_id] = preprocess(text)
            update.message.reply_text(
                '更改店家名稱為{}\n請傳送照片或重新輸入名稱'.format(add_query_shopname[chat_id])
            )

            
        print('status:', status)
    except KeyError:
        print('ignore it')
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def whengetphoto(update, bot):  
    chat_id = getID(update)
    try:
        state = status[chat_id]
        if state == 'add_step2':
            update.message.reply_text(
                '正在取得照片...'
            )
            photorequesturl = 'https://api.telegram.org/bot' + os.getenv("TELEGRAM_TOKEN") + '/getfile?file_id=' + update.message.photo[0].file_id
            photolink = uploadAndGetPhoto(photorequesturl)
            if chat_id in add_query_photolink:
                print("EXIST")
                add_query_photolink[chat_id].append(photolink)
            else:
                print("NONE")
                add_query_photolink[chat_id] = [photolink]
                
            update.message.reply_text(
                '請繼續傳送照片或輸入 /add 結束傳送'
            )

        print('status:', status)
    except KeyError:
        print('ignore it')
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def whengetfile(update, bot):
    chat_id = getID(update)
    try:
        state = status[chat_id]
        if state == 'add_step2':
            update.message.reply_text(
                '正在取得照片...'
            )
            photorequesturl = 'https://api.telegram.org/bot' + os.getenv("TELEGRAM_TOKEN") + '/getfile?file_id=' + update.message.document.file_id
            photolink = uploadAndGetPhoto(photorequesturl)
            if chat_id in add_query_photolink:
                print("EXIST")
                add_query_photolink[chat_id].append(photolink)
            else:
                print("NONE")
                add_query_photolink[chat_id] = [photolink]
                
            update.message.reply_text(
                '請繼續傳送照片或輸入 /add 結束傳送'
            )

        print('status:', status)
    except KeyError:
        print('ignore it')
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def addtag(update, bot):
    if isDos(update): return
    chat_id = update.message.chat_id
    try:
        command, shopname, tag = update.message.text.split()
    except ValueError:
        update.message.reply_text(
            '輸入格式為 /addtag 店家 標籤'
        )
        return
    shopname = preprocess(shopname)
    tag = preprocess(tag)

    list = getshops()
    if not shopname in list:
        update.message.reply_text(
            '無此店家'
        )
        update.message.reply_text(
            '可先用 /search 查詢正確名稱'
        )
        return
    else:
        tags = get_tags(shopname)
        if tag in tags:
            update.message.reply_text(
                '重複的標籤'
            )
            return
        else:
            tags.append(tag)
            update.message.reply_text(
                '正在新增標籤...'
            )
            update_tag(shopname, tags)
            update.message.reply_text(
                '在{}上新增標籤{}，新增完成。'.format(shopname, tag)
            )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def clearallrequest(update, bot):
    if isDos(update): return

    chat_id = getID(update)

    if(chat_id in status):
        del(status[chat_id])

    if(chat_id in add_query_shopname):
        del(add_query_shopname[chat_id])

    if(chat_id in add_query_classification):
        del(add_query_classification[chat_id])

    if(chat_id in add_query_photolink):
        del(add_query_photolink[chat_id])
    
    update.message.reply_text(
        "已清除您的所有要求"
    )
    print('status', status)
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def listall(update, bot):
    if isDos(update): return
    list = getshops()
    ret = ''
    count = 0
    for i in list:
        ret += i
        count +=1
        if(count==4):
            count = 0
            ret += '\n'
        else:
            if(len(i)>6):
                ret+='\n'
            else:
                for j in range(7-len(i)):
                    ret += '\t\t\t\t'
    update.message.reply_text(
        ret
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def getID(update):
    return str(update.message.from_user.id)

def report(update, bot):
    if isDos(update): return
    name = update.message.from_user.full_name
    try:
        text = update.message.text.split('/report ')[1]
    except IndexError:
        update.message.reply_text(
            '請使用以下格式回報問題：\n' + '/report 回報內容\n'
        )
        return

    chat_type = update.message.chat.type

    fp2 = codecs.open("user_report.txt", "a", "utf-8")
    fp2.write('{} as {}: {}\n'.format(name, chat_type, text))
    fp2.close()
    update.message.reply_text(
        '已將您的問題回報給開發者，感謝您的使用'
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def appendlog(user_id, username, text):
    fp2 = codecs.open("logger.txt", "a", "utf-8")
    fp2.write('{}({}): {}\n'.format(user_id, username, text))
    fp2.close()