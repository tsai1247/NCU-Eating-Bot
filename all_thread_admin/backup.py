from checkpermission import checkpermission
from fileRW import write
from appendlog import appendlog
from dosdefence import getID, isDos
from interact_with_hackmd import getcode
from variable import *
import threading

class thread_backup(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return

        write("filename_back_up.txt", getcode())
        update.message.reply_text(
            "手動備份完成"
        )
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
