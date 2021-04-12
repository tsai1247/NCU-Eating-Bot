#!/usr/bin/env python3
# coding=UTF-8
from functions.fileRW import append
from functions.interact_with_imgur import uploadAndGetPhoto
from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading


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

class thread_file(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        
        if isDos(update): return
        DealWithPhotolink(update, update.message.document.file_id) 
        appendlog(getID(update), update.message.from_user.full_name, 'getfile')