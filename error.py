from functions.fileRW import append

def error(update, context, **kwargs):
    msg = 'default msg.'
    try:
        error = context.error
        msg = 'Error from {}.\nError type: {}.\nError message: {}\n'.format(update.message.chat_id, type(error), str(error.message))
    except:
        try:
            msg = 'Error from {}.\nError message: {}\n'.format(update.message.chat_id, str(error.message))
        except:
            try:
                msg = 'Error from {}.\n'.format(update.message.chat_id)
            except:
                msg = 'Error\n'
    append('logger.txt', msg)
    update.message.reply_text('未知異常發生，請稍後再試。\n如有問題請使用 /report 指令\n或洽 jeff29cc91079@gmail.com ，謝謝')