from fileRW import append

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