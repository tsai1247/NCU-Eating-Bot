from all_thread_admin.importall import *

# functions for commands
def backup(update, bot):
    thread_backup(update, bot).start()
    
def undo(update, bot):
    thread_undo(update, bot).start()

def restore(update, bot):
    thread_restore(update, bot).start()

def xhelp(update, bot):
    thread_xhelp(update, bot).start()

def xhelpzh(update, bot):
    thread_xhelpzh(update, bot).start()

def addtypo(update, bot):
    thread_addtypo(update, bot).start()

def test(bot, update):
    thread_test(update, bot).start()

def getreport(update, bot):
    thread_getreport(update, bot).start()

def manual_overwrite(update, bot):
    thread_overwrite(update, bot).start()
