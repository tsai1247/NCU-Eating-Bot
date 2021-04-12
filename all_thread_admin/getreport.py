from fileRW import Concat_Lines, read
from checkpermission import checkpermission
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading


def singleReport(update, num):
    if num==1:
        report_files = read('user_report.txt')
        update.message.reply_text('User Report:')
        for i in range(int(len(report_files)/30)):
            update.message.reply_text(Concat_Lines(report_files[i*30:(i+1)*30]))
        if len(report_files)>0:
            update.message.reply_text(Concat_Lines(report_files[int(len(report_files)/30)*30:]))
    elif num==2:
        shop_files = read('non-exist-shop.txt')
        update.message.reply_text('Non exist shops:')
        for i in range(int(len(shop_files)/30)):
            update.message.reply_text(Concat_Lines(shop_files[i*30:(i+1)*30]))
        if len(shop_files)>0:
            update.message.reply_text(Concat_Lines(shop_files[int(len(shop_files)/30)*30:]))
    elif num==3:
        logger_files = read('logger.txt')
        update.message.reply_text('Logger:')
        for i in range(int(len(logger_files) /30)):
            update.message.reply_text(Concat_Lines(logger_files[i*30:(i+1)*30]))
        if len(logger_files)>0:
            update.message.reply_text(Concat_Lines(logger_files[int(len(logger_files)/30)*30:]))
    else:
        update.message.reply_text('type error.')

class thread_getreport(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return

        chat_id = getID(update)
    
        text = update.message.text.split()
        if len(text)>2:
            update.message.reply_text('type error.')
        elif len(text) == 2:
            if not text[1].isdecimal():
                update.message.reply_text('type error.')
            else:
                singleReport(update, int(text[1]))
        else:
            for i in range(1,4):
                singleReport(update, i)
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)