#!/usr/bin/env python3
# coding=UTF-8
import random
from requests.models import parse_header_links
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os
from dotenv import load_dotenv
import json
import pyimgur



# preparation
load_dotenv() # Loading environment variable from .env file
url = os.getenv("MD_SOURCE")
status = {}


def isempty(st):
    num = st.count(' ')+st.count('\n')+st.count(':')+st.count('-')
    return (num==len(st))

def getMenu(shopname):  # return a list including all menus to shopname
    code = getcode()
    urls = code.split('### ' + shopname)[1].split('###')[0].split('![]')
    lst = []
    for i in range(1, len(urls)):
        pic = urls[i].split('(')[1].split(')')[0]
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
    # bot.send_photo(
    #     chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')

def help_zh(update, bot):
   
    update.message.reply_text(
        '以下是常用的指令: \n'
        '/help : English document\n'
        '/helpzh : 查看此說明。\n'
        '/random : 隨機取得一個菜單。\n'
        '/search : 查詢菜單。\n'
        '/add : 新增菜單(未完成)。\n'
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
    pass
    

def search(update, bot):
    chat_id = update.message.chat_id
    status[chat_id] = "search"
    update.message.reply_text(
        '請輸入店家名稱'
    )
    print('status:', status)

def filtermsg(update, bot):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        state = status[chat_id]
        if(state == 'search'):
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

        del(status[chat_id])
        print('status:', status)
    except KeyError:
        print('ignore it')

def whengetphoto(update, bot):  
    photorequesturl = 'https://api.telegram.org/bot' + os.getenv("TELEGRAM_TOKEN") + '/getfile?file_id=' + update.message.photo[0].file_id
    photoresponse =  json.loads(requests.get(photorequesturl).content.decode())
    file_path = photoresponse['result']['file_path']
    # when error 404?
    photorequesturl = 'https://api.telegram.org/file/bot' + os.getenv("TELEGRAM_TOKEN") + '/' + file_path
    photo = requests.get(photorequesturl).content
    fp = open("tmpphoto.png", "wb")
    fp.write(photo)
    fp.close()
    
    CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
    PATH = "tmpphoto.png"
    title = "Uploaded with PyImgur"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type)
    
    fp = open("filename.txt", "w")
    fp.write('![](' + uploaded_image.link + ')\n')
    fp.close()
    
    command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' filename.txt'
    print(command, end='\n\n')
    os.system(command)
    


    print('here')
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
    updater.dispatcher.add_handler(MessageHandler(Filters.text, filtermsg))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, whengetphoto))

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
