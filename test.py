from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

url = 'https://hackmd.io/Tz5EFYy-T-Sp9LqpvJkGLg?edit'

def getcode(hackmdurl):
  response = requests.get(hackmdurl)
  sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
  code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
  return code

# TODO: the functions corresponding to each keyword
def hello(update, bot):
    update.message.reply_text(
        'hello, {}'.format(update.message.from_user.first_name))

def help(update, bot):
   
    update.message.reply_photo(
        'https://i.imgur.com/C4UDohi.jpg'
    )
    # bot.send_photo(
    #     chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')

def filtermsg(update, bot):
    chat_id = update.message.chat_id
    update.message.reply_text(
        update.message.text + ' hihi~~ ' + (str)(chat_id)
    )
    # bot.send_photo(
    #     chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')


# Main
def main():
    updater = Updater('1562606203:AAHpn9Z3DNjQcoqdGDujSLnm53ji2_AjNsM')
    

# TODO: declaration of keywords
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('start', help))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, filtermsg))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



"""
reference:

https://core.telegram.org/bots/api#sendmessage method
    $message = <<<TEXT
    *** your content ***
    *** somewhere below (or above) a link to your image with invisible character(s) ***
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