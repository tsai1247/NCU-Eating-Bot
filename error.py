from fileRW import append

def error(update, context, **kwargs):
    try:
        error = context.error
        msg = 'Error from {}.\n Error type: {}.\n Error message: {}\n'.format(update.message.chat_id, type(error), str(error.message))
        append('logger.txt', msg)
    except:
        append('logger.txt', 'Error\n')