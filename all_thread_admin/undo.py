from fileRW import Concat_Lines, read, write
from overwrite import overwrite
from checkpermission import checkpermission
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_undo(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        if(not checkpermission(update)):   return

        update.message.reply_text("還原中...")
        overwrite('filename_auto_back_up.txt')
        curData = Concat_Lines(read('filename.txt'))
        write('filename.txt', Concat_Lines(read('filename_auto_back_up.txt')))
        write('filename_auto_back_up.txt', curData)

        update.message.reply_text("以自動備份檔還原完成")

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
