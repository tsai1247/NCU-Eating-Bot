#!/usr/bin/env python3
# coding=UTF-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from dotenv import load_dotenv

from admin import *
from interact_with_hackmd import *
from command import *

# preparation
load_dotenv() # Loading environment variable from .env file

# Main
def main():
    updater = Updater( os.getenv("TELEGRAM_TOKEN") )

# TODO: declaration of keywords
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('helpzh', help_zh))
    updater.dispatcher.add_handler(CommandHandler('random', randomfunc))
    updater.dispatcher.add_handler(CommandHandler('add', add))
    updater.dispatcher.add_handler(CommandHandler('search', search))
    updater.dispatcher.add_handler(CommandHandler('test', test))
    
    # admin commands
    updater.dispatcher.add_handler(CommandHandler('xhelp', xhelp))
    updater.dispatcher.add_handler(CommandHandler('xhelpzh', xhelpzh))
    updater.dispatcher.add_handler(CommandHandler('clear', clearallrequest))
    updater.dispatcher.add_handler(CommandHandler('backup', backup))
    updater.dispatcher.add_handler(CommandHandler('undo', undo))
    updater.dispatcher.add_handler(CommandHandler('restore', restore))

    # normal messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, filtermsg))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, whengetphoto))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, whengetfile))

    # calbackhandler
    updater.dispatcher.add_handler(CallbackQueryHandler(getClassification))

    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



"""
reference:

https://core.telegram.org/bots/api#sendmessage method
    $message = <<<TEXT
    *** your content ***
    *** somew
    here below (or above) a link to your image with invisible character(s) ***
    <a href="https://www.carspecs.us/photos/c8447c97e355f462368178b3518367824a757327-2000.jpg"> ‏ </a>
    TEXT;

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: multipart/form-data']);
    curl_setopt($ch, CURLOPT_URL, 'https://api.telegram.org/bot<token>/sendMessage');
    $postFields = array(
        'chat_id' => '@username',
        'text' => $message,
        'parse_mode' => 'HTML',
        'disable_web_page_preview' => false,
    );
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
    if(!curl_exec($ch))
        echo curl_error($ch);
    curl_close($ch);


https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-an-image-file-from-disk :

    bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')

MessageHandler(Filters.text, reply_handler)

chat_id = bot.get_updates()[-1].message.chat_id

"""
