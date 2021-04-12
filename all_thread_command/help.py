from appendlog import appendlog
from dosdefence import getID, isDos
from variable import help_en
import threading

class thread_help(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot

    def run(self):
        update = self.update
        bot = self.bot
        if isDos(update): return
        update.message.reply_text(help_en)
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
