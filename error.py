import codecs


def error(update, context, **kwargs):
    """ Error handling """
    try:
        error = context.error
        fp2 = codecs.open("logger.txt", "a", "utf-8")
        fp2.write('Error from {}.\n Error type: {}.\n Error message: {}\n'.format(update.message.chat_id, type(error), str(error.message)))
        fp2.close()

    except:
        fp3 = codecs.open("logger.txt", "a", "utf-8")
        fp3.write('Error\n')
        fp3.close()