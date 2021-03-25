import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from interact_with_hackmd import *
from interact_with_imgur import *

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