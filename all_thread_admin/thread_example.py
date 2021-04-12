from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_example(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        