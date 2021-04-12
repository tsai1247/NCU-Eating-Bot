from fileRW import read, write
from checkpermission import checkpermission
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_addtypo(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot

        if isDos(update): return
        if(not checkpermission(update)):   return

        correct, wrong = update.message.text[len('/addtypo '):].split()
        r = read("typo.json")
        if correct in r:    r[correct].append(wrong)
        else:   r[correct] = [wrong]
        r = str(r)
        r = r.replace("\'", "\"")
        write("typo.json", r)
        update.message.reply_text("已新增")

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
