from telegram.ext import Updater, CommandHandler

def hello(update, bot):
    update.message.reply_text(
        'hello, {}'.format(update.message.from_user.first_name))


updater = Updater('1562606203:AAHpn9Z3DNjQcoqdGDujSLnm53ji2_AjNsM')

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()