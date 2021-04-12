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