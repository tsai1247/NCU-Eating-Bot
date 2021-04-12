from checkpermission import checkpermission
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_test(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return
        
        print('hi')
        chat_id = getID(update)
        text = 'hihi~~'    
        # bot.send_message(chat_id, text)
        update.message.reply_text(update.toString())
        # appendlog(getID(update), update.message.from_user.full_name, update.message.text)