from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_example(threading.Thread):
    def __init__(self, update):
        threading.Thread.__init__(self)
        self.update = update
        
    def run(self):
        update = self.update
        appendlog(getID(update), update.message.from_user.full_name, update.message.text)
