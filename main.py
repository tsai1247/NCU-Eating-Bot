#!/usr/bin/env python3
# coding=UTF-8
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Loading environment variable from .env file

url = os.getenv("MD_SOURCE")
status = {}


def isempty(st):
    num = st.count(' ')+st.count('\n')+st.count(':')+st.count('-')
    return (num==len(st))

def getMenu(shopname):
    code = getcode(url)
    urls = code.split('### ' + shopname)[1].split('###')[0]
    lst = []
    for i in urls.split('![]'):
        lst.append(i.split('(')[1].split(' =400x')[0])
    return lst
    
def getcode():
  response = requests.get(url)
  sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
  code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
  return code

def getlist():
    code = getcode()
    list = code.split('## 索引')[1].split('## 宵夜街')[0]
    return list

def getshops():
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
        '/add : add new menu.\n'
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
        '/add : 新增菜單。\n'
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
                getcode(url)
    )))
    
def add(update, bot):
    print('add')


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
            list = getshops(url)
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
            print(list)

        del(status[chat_id])
        print('status:', status)
    except KeyError:
        print('ignore it')

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
