from functions.dosdefence import getID
import os

def checkpermission(update):
    chat_id = getID(update)
    developer_id = os.getenv("DEVELOPER_ID").split(',')
    if chat_id in developer_id:
        return True
    else:
        update.message.reply_text("你沒有使用此指令的權限")
        update.message.reply_text("但名豐可以請客")
        return False

def checkLowerPermission(update):
    chat_id = getID(update)
    lower_permission_id = os.getenv("LOWER_PERMISSION_ID").split(',')
    if checkpermission(update):
        return True
    elif chat_id in lower_permission_id:
        return True
    else:
        update.message.reply_text("你沒有使用此指令的權限")
        update.message.reply_text("但名豐可以請客")
        return False

