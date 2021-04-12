from appendlog import appendlog
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from interact_with_hackmd import updateHackmd
from interact_with_imgur import getNoMenuLink
from dosdefence import getID, isDos
from variable import *
import threading

class thread_add(threading.Thread):
    def __init__(self, update):
        threading.Thread.__init__(self)
        self.update = update
        
    def run(self):
        with self.update as update:
            if isDos(update): return
            
            chat_id = getID(update)
            if status.get(chat_id) == "add_step2":
                status.pop(chat_id)
                update.message.reply_text('正在新增店家...')
                cur_classification = add_query_classification.get(chat_id)
                cur_shopname = add_query_shopname.get(chat_id)
                if(chat_id in add_query_photolink):
                    cur_photolink = add_query_photolink.get(chat_id)
                else:
                    cur_photolink = [getNoMenuLink()]
                updateHackmd(chat_id, cur_classification, cur_shopname, cur_photolink)
                update.message.reply_text('新增店家 {} 於分類 {}, 新增完成。'.format(cur_shopname, cur_classification))
            else:
                add_query_update.update({chat_id:update})
                status.update({chat_id:'add_step0'})
                update.message.reply_text("請選擇分類",
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 0)) for s in list(classMap.keys())[0::2]],
                        [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 0)) for s in list(classMap.keys())[1::2]]
                    ]))

            appendlog(getID(update), update.message.from_user.full_name, update.message.text)
