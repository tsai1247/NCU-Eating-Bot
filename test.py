import telebot
bot = telebot.TeleBot('1562606203:AAHpn9Z3DNjQcoqdGDujSLnm53ji2_AjNsM')
@bot.message_handler(commands=['start'])
def handle_command(message):
    bot.reply_to(message, "Hello, welcome to Telegram Bot!")

bot.polling()



# '1562606203:AAHpn9Z3DNjQcoqdGDujSLnm53ji2_AjNsM'