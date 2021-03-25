#!/usr/bin/env python3
# coding=UTF-8
from logging import exception
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os
from dotenv import load_dotenv
import json
import pyimgur
import codecs

# preparation
load_dotenv() # Loading environment variable from .env file
url = os.getenv("MD_SOURCE")
status = {}
add_query_classification = {}
add_query_shopname = {}
add_query_photolink = {}
classMap = {'宵夜街':2, '後門':3, '奢侈接':4, '山下':5}

def isDEVELOPER(chat_id):
    developer_id = os.getenv("DEVELOPER_ID").split(',')
    if chat_id in developer_id:
        return True
    else:
        return False

def updateHackmd(chat_id, classification, shopname, photolink):
    def GetReverseMenu(curMenu):
        midpath = []
        for i in range(len(curMenu[0])):
            midpath.append([])

        for i in curMenu:
            # print(i)
            for j in range(len(i)):
            # print('>', j)
                midpath[j].append(i[j])
        return midpath

    def getMDtable(reverseMenu):
        ret = ''
        for i in reverseMenu:
            ret+='|'
            for j in i:
               ret+= j + '|'
            ret+='\n'

        return ret
    
    def updateIndex(code, index):
        undealtlist = code.split('|')[1:]

        dealtlist = []
        for i in range(int(len(undealtlist)/5)):
            dealtlist.append([])
            for j in range(4):
                dealtlist[-1].append(undealtlist[i*5+j])

        reverseMenu = GetReverseMenu(dealtlist)
        
        for i in range(len(reverseMenu[index])):
            if(reverseMenu[index][i]==''):
                reverseMenu[index][i]= '[{}](##{})'.format(shopname, shopname)
                break
            elif i+1==len(reverseMenu[index]):
                reverseMenu[index].append('[{}](##{})'.format(shopname, shopname))
                for j in range(4):
                    if(j!=index):
                        reverseMenu[j].append('')
        
        reverseMenu = GetReverseMenu(reverseMenu)
        
        ret = getMDtable(reverseMenu)
        ret = '## 索引\n' + ret
        return ret

    def updatePhoto(code):
        code += '### {}\n'.format(shopname)
        for i in photolink:
            code += '![]({} =400x)\n'.format(i)
        code += '\n'
        return code
    del(add_query_classification[chat_id])
    del(add_query_shopname[chat_id])
    del(add_query_photolink[chat_id])
    code = split(getcode()) # len = 6
                            # 菜單 索引 宵夜街 後門 奢侈街 山下
    index = classMap[classification]
    code[1] = updateIndex(code[1], index-2)
    code[index] = updatePhoto(code[index])
    newcode = ''
    for i in code:
        newcode += i
    
    fp = codecs.open("filename.txt", "r", "utf-8")
    oldcode = fp.readlines
    print(oldcode)
    fp.close()

    fp2 = codecs.open("filename_auto_back_up.txt", "w", "utf-8")
    fp2.write(oldcode)
    fp2.close()

    fp = codecs.open("filename.txt", "w", "utf-8")
    fp.write(newcode)
    fp.close()
    
    

    command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' filename.txt'
    os.system(command)


def uploadAndGetPhoto(photorequesturl):
    photoresponse =  json.loads(requests.get(photorequesturl).content.decode())
    file_path = photoresponse['result']['file_path']
    # when error 404?
    photorequesturl = 'https://api.telegram.org/file/bot' + os.getenv("TELEGRAM_TOKEN") + '/' + file_path
    print(photorequesturl)
    photo = requests.get(photorequesturl).content
    fp = open("tmpphoto.png", "wb")
    fp.write(photo)
    fp.close()
    
    CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
    PATH = "tmpphoto.png"
    title = "Uploaded with PyImgur"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    return uploaded_image.link

def isempty(st):
    num = st.count(' ')+st.count('\n')+st.count(':')+st.count('-')
    return (num==len(st))

def split(code):
    ret = []
    tmp = code

    ret.append(tmp.split('## 索引')[0])
    tmp = '## 索引' + tmp.split('## 索引')[1]

    ret.append(tmp.split('## 宵夜街')[0])
    tmp = '## 宵夜街' + tmp.split('## 宵夜街')[1]

    ret.append(tmp.split('## 後門')[0])
    tmp = '## 後門' + tmp.split('## 後門')[1]

    ret.append(tmp.split('## 奢侈街')[0])
    tmp = '## 奢侈街' + tmp.split('## 奢侈街')[1]

    ret.append(tmp.split('## 山下')[0])
    tmp = '## 山下' + tmp.split('## 山下')[1]

    ret.append(tmp)
    return ret

def getMenu(shopname):  # return a list including all menus to shopname
    code = getcode()
    urls = code.split('### ' + shopname)[1].split('###')[0].split('![]')
    lst = []
    for i in range(1, len(urls)):
        pic = urls[i].split('(')[1].split(' =400x)')[0]
        lst.append(pic)
    return lst

def getcode():  # get all hackmd contents
  response = requests.get(url)
  sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
  code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
  return code

def getlist():  # return the table of "索引" on hackmd
    code = getcode()
    list = code.split('## 索引')[1].split('## 宵夜街')[0]
    return list

def getshops():   # return a list including all shops
    tmp = getlist().split('|')[6:-1]
    list = []
    for i in tmp:
        if(not isempty(i)):
            list.append(i.split('[')[1].split(']')[0])
    return list

# TODO: the functions corresponding to each keyword

def start(update, bot):
    curName =  update.message.from_user.username
    update.message.reply_text(
        'Hello, ' +
        curName +
        '.'
    )
    update.message.reply_text(
        'I am just a Eating Bot.'
    )
    help(update, bot)
    # bot.send_photo(
    #     chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')

def help(update, bot):
   
    update.message.reply_text(
        'The followings are some commands: \n'
        '/helpzh : 查看中文說明\n'
        '/help : get this document.\n'
        '/random : get a random restaurant menu.\n'
        '/search : search a menu.\n'
        '/add : add new menu(not done).\n'
    )

def help_zh(update, bot):
   
    update.message.reply_text(
        '以下是常用的指令: \n'
        '/help : English document\n'
        '/helpzh : 查看此說明。\n'
        '/random : 隨機取得一個菜單。\n'
        '/search : 查詢菜單。\n'
        '/add : 新增菜單(未完成)。\n'
    )


def xhelp(update, bot):
    chat_id = str(update.message.chat_id)
    if(not isDEVELOPER(chat_id)):
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        update.message.reply_text(
            "但名豐可以請客"
        )
        return

    update.message.reply_text(
        'The followings are some commands: \n'
        '/xhelpzh : 查看中文管理員指令說明\n'
        '/xhelp : get this document.\n'
        '/clear : (debug tool) reset all variable about chat id.\n'
        '/backup : manually backup a hackmd data.\n'
        '/undo : overwrite hackmd data with auto_backup data.\n'
        '/restore : overwrite hackmd data with manual_backup data.\n'
    )

def xhelpzh(update, bot):
    chat_id = str(update.message.chat_id)
    if(not isDEVELOPER(chat_id)):
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        return

    update.message.reply_text(
        '以下是管理員指令: \n'
        '/xhelpzh : 查看此說明\n'
        '/xhelp : get English document for administrator\'s commands\n'
        '/clear : (除錯工具) 重置關於此 chat_id 的所有狀態\n'
        '/backup : 手動備份資料。\n'
        '/undo : 從上次的自動備份還原菜單。\n'
        '/restore : 從上次的手動備份還原菜單。\n'
    )

def randomfunc(update, bot):
   
    def random_menu(code):
        rd = code.split('###')
        ret = rd[random.randint(1, len(rd)-1)].split('###')[0]
        return ret
    def sort(rand_shop):
        cur = rand_shop.split('![]')
        for i in range(1, len(cur)):
            cur[i] = cur[i].split('(')[1].split(' =400x')[0]
        return cur
    def push_menu(sorted_shop):
        update.message.reply_text(
            sorted_shop[0]
        )
        for i in range(1, len(sorted_shop)):
            update.message.reply_photo(
                sorted_shop[i]
            )

    push_menu(
        sort(
            random_menu(
                getcode()
    )))
    
def add(update, bot):
    chat_id = str(update.message.chat_id)
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
                '新增店家 {} 於分類 {}, 新增完成。'.format(cur_classification, cur_shopname)
            )

    except KeyError:
        update.message.reply_text("請選擇分類",
            reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton(s, callback_data = '{} {}'.format(s, chat_id)) for s in ['宵夜街', '後門', '奢侈街', '山下']
                ]]))

   

    print('status:', status)

def getClassification(update, bot):
    s, chat_id = update.callback_query.data.split(" ")
    update.callback_query.edit_message_text(
        '分類為：{}\n請輸入店家名稱'.format(s)
    )
    status[chat_id] = "add_step1"
    add_query_classification[chat_id] = s
    print('status:', status)

def search(update, bot):
    chat_id = str(update.message.chat_id)
    status[chat_id] = "search"
    update.message.reply_text(
        '請輸入店家名稱'
    )
    print('status:', status)

def filtermsg(update, bot):
    chat_id = str(update.message.chat_id)
    text = update.message.text
    try:
        state = status[chat_id]
        if state == 'search':
            del(status[chat_id])
            list = getshops()
            try:
                list.index(text)
                curMenu = getMenu(text)
                for i in curMenu:
                    update.message.reply_photo(
                        i
                    )
            except ValueError:
                update.message.reply_text(
                    '此店家不存在'
                )
        elif state == 'add_step1':
            del(status[chat_id])
            status[chat_id] = "add_step2"
            add_query_shopname[chat_id] = text
            update.message.reply_text(
                '新增店家名稱為{}\n請傳送照片或重新輸入名稱'.format(add_query_shopname[chat_id])
            )
        elif state == 'add_step2':
            del(status[chat_id])
            status[chat_id] = "add_step2"
            del(add_query_shopname[chat_id])
            add_query_shopname[chat_id] = text
            update.message.reply_text(
                '新增店家名稱為{}\n請傳送照片或重新輸入名稱'.format(add_query_shopname[chat_id])
            )

            
        print('status:', status)
    except KeyError:
        print('ignore it')

def whengetphoto(update, bot):  
    chat_id = str(update.message.chat_id)
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

def whengetfile(update, bot):
    chat_id = str(update.message.chat_id)
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



def clearallrequest(update, bot):
    chat_id = str(update.message.chat_id)
    if(not isDEVELOPER(chat_id)):
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        return

    try:
        del(status[chat_id])
    except KeyError:
        print('ignore it')
    try:
        del(add_query_shopname[chat_id])
    except KeyError:
        print('ignore it')
    try:
        del(add_query_classification[chat_id])
    except KeyError:
        print('ignore it')
    try:
        del(add_query_photolink[chat_id])
    except KeyError:
        print('ignore it')
    
    update.message.reply_text(
        "已清除您的所有要求"
    )

def backup(update, bot):
    chat_id = str(update.message.chat_id)
    if(not isDEVELOPER(chat_id)):
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        return

    fp = codecs.open("filename.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()
    
    fp2 = codecs.open("filename_back_up.txt", "w", "utf-8")
    for i in oldcode:
        fp2.write(i)
    fp2.close()

    update.message.reply_text(
        "手動備份完成"
    )

def undo(update, bot):
    chat_id = str(update.message.chat_id)
    if(not isDEVELOPER(chat_id)):
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        return

    update.message.reply_text(
        "還原中..."
    )
    
    command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' filename_auto_back_up.txt'
    os.system(command)

    update.message.reply_text(
        "以自動備份檔還原完成"
    )

def restore(update, bot):
    chat_id = str(update.message.chat_id)
    if(not isDEVELOPER(chat_id)):
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        return

    update.message.reply_text(
        "還原中..."
    )

    command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' filename_back_up.txt'
    os.system(command)

    update.message.reply_text(
        "以手動備份檔還原完成"
    )
        
        

# Main
def main():
    updater = Updater( os.getenv("TELEGRAM_TOKEN") )

# TODO: declaration of keywords
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('helpzh', help_zh))
    updater.dispatcher.add_handler(CommandHandler('random', randomfunc))
    updater.dispatcher.add_handler(CommandHandler('add', add))
    updater.dispatcher.add_handler(CommandHandler('search', search))
    
    # debugging tools
    updater.dispatcher.add_handler(CommandHandler('xhelp', xhelp))
    updater.dispatcher.add_handler(CommandHandler('xhelpzh', xhelpzh))
    updater.dispatcher.add_handler(CommandHandler('clear', clearallrequest))
    updater.dispatcher.add_handler(CommandHandler('backup', backup))
    updater.dispatcher.add_handler(CommandHandler('undo', undo))
    updater.dispatcher.add_handler(CommandHandler('restore', restore))

    # normal messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, filtermsg))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, whengetphoto))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, whengetfile))

    # calbackhandler
    updater.dispatcher.add_handler(CallbackQueryHandler(getClassification))



    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



"""
reference:

https://core.telegram.org/bots/api#sendmessage method
    $message = <<<TEXT
    *** your content ***
    *** somewhere below (or above) a link to your image with invisible character(s) ***
    <a href="https://www.carspecs.us/photos/c8447c97e355f462368178b3518367824a757327-2000.jpg"> ‏ </a>
    TEXT;

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: multipart/form-data']);
    curl_setopt($ch, CURLOPT_URL, 'https://api.telegram.org/bot<token>/sendMessage');
    $postFields = array(
        'chat_id' => '@username',
        'text' => $message,
        'parse_mode' => 'HTML',
        'disable_web_page_preview' => false,
    );
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
    if(!curl_exec($ch))
        echo curl_error($ch);
    curl_close($ch);


https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-an-image-file-from-disk :

    bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')

MessageHandler(Filters.text, reply_handler)

chat_id = bot.get_updates()[-1].message.chat_id

"""
