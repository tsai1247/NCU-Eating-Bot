#!/usr/bin/env python3
# coding=UTF-8
import os
from dotenv import load_dotenv

load_dotenv() # Loading environment variable from .env file

# normal variable
url = os.getenv("MD_SOURCE")
status = {}
add_query_classification = {}
add_query_shopname = {}
add_query_update = {}
add_query_photolink = {}
classMap = {'宵夜街':2, '後門':3, '奢侈街':4, '山下':5}
# classMap = {'宵夜街':2, '後門':3, '奢侈街':4, '山下':5, '校內':6}
ignore_list = [' ', '\n', '\t']

# variable about dos defence
dos_maximum = 25
penalty = 300
dos_defence= {}

# help documents
xhelp_en = 'The followings are some commands: \n\
            /xhelpzh : 查看中文管理員指令說明\n\
            /xhelp : get this document.\n\
            /clear : (debug tool) reset all variable about chat id.\n\
            /backup : manually backup a hackmd data.\n\
            /undo : overwrite hackmd data with auto_backup data.\n\
            /restore : overwrite hackmd data with manual_backup data.\n\
            /addtypo correct_text wrong_text : stronger search function.\n'

xhelp_zh =  '以下是管理員指令: \n\
            /xhelpzh : 查看此說明\n\
            /xhelp : get English document for administrator\'s commands\n\
            /clear : (除錯工具) 重置關於此 chat_id 的所有狀態\n\
            /backup : 手動備份資料。\n\
            /undo : 從上次的自動備份還原菜單。\n\
            /restore : 從上次的手動備份還原菜單。\n\
            /addtypo 正確詞 錯誤詞 : 新增常見錯字資料。\n'

help_en =   'The followings are some commands: \n\
            /helpzh : 查看中文說明\n\
            /help : get this document.\n\
            /random : get a random restaurant menu.\n\
            /search : search a menu.\n\
            /add : add new menu.\n\
            /list : list all menu.\n\
            /addtag : add tag for a shop.\n\
            /report: report the bot\'s problems\n'

help_zh =   '以下是常用的指令: \n\
            /help : English document\n\
            /helpzh : 查看此說明。\n\
            /random : 隨機取得一個菜單。\n\
            /search : 查詢菜單。\n\
            /add : 新增菜單。\n\
            /list : 列出所有店家。\n\
            /addtag : 在店家上新增標籤。\n\
            /report: 回報Bot的問題。\n'

hint_zh =   [   '在 Telegram Desktop 上，選擇圖片檔後，取消勾選Compress images再傳送',
                '在 Telegram App 上，使用 file -> Gallery 選擇並傳送圖片檔',
                '在 Telegram Web 上，使用 Send file 選擇並傳送圖片檔'
            ]
