from functions.fileRW import append

def appendlog(user_id, username, text):
    append('logger.txt', '{}({}): {}\n'.format(user_id, username, text))
