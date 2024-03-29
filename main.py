#!/usr/bin/env python3
# coding=UTF-8
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from dotenv import load_dotenv

from admin import *
from command import *
from protectedCommand import *
from error import *

# preparation
load_dotenv() # Loading environment variable from .env file

# Main
def main():
    updater = Updater( os.getenv("TELEGRAM_TOKEN") )

    # TODO: declaration of keywords
    # all_thread_command
    updater.dispatcher.add_handler(CommandHandler('start', startbot))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('helpzh', helpzh))
    updater.dispatcher.add_handler(CommandHandler('random', randomfunc))
    updater.dispatcher.add_handler(CommandHandler('add', add))
    updater.dispatcher.add_handler(CommandHandler('search', search))
    # updater.dispatcher.add_handler(CommandHandler('tag', tag))
    updater.dispatcher.add_handler(CommandHandler('addtag', addtag))
    updater.dispatcher.add_handler(CommandHandler('list', listall))
    updater.dispatcher.add_handler(CommandHandler('listall', listall))
    updater.dispatcher.add_handler(CommandHandler('report', report))
    updater.dispatcher.add_handler(CommandHandler('hint', hint))
    updater.dispatcher.add_handler(CommandHandler('electric', electric))

    # all_thread_protectedcommand
    updater.dispatcher.add_handler(CommandHandler('delete', delete))
    updater.dispatcher.add_handler(CommandHandler('del', delete))
    updater.dispatcher.add_handler(CommandHandler('modify', edit))
    updater.dispatcher.add_handler(CommandHandler('edit', edit))

    # all_thread_admin
    updater.dispatcher.add_handler(CommandHandler('xhelp', xhelp))
    updater.dispatcher.add_handler(CommandHandler('xhelpzh', xhelpzh))
    updater.dispatcher.add_handler(CommandHandler('clear', clearallrequest))
    updater.dispatcher.add_handler(CommandHandler('backup', backup))
    updater.dispatcher.add_handler(CommandHandler('undo', undo))
    updater.dispatcher.add_handler(CommandHandler('restore', restore))
    updater.dispatcher.add_handler(CommandHandler('addtypo', addtypo))
    updater.dispatcher.add_handler(CommandHandler('test', test))
    updater.dispatcher.add_handler(CommandHandler('getreport', getreport))
    updater.dispatcher.add_handler(CommandHandler('overwrite', manual_overwrite))

    # normal messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, whengettext))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, whengetphoto))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, whengetfile))

    # callbackhandler
    updater.dispatcher.add_handler(CallbackQueryHandler(callback))

    # error handler
    updater.dispatcher.add_error_handler(error)

    print("Server Running...")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


'''
reference:

https://core.telegram.org/bots/api#sendmessage
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-an-image-file-from-disk

'''
