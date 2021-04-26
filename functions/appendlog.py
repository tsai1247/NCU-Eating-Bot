from functions.fileRW import append
import time

def appendlog(user_id, username, text):
    append('logger.txt', '[{}] {}({}): {}\n'.format(time.strftime('%Y/%m/%d\t%H:%M:%S'), user_id, username, text))
