import codecs
import json

from requests import check_compatibility
from interact_with_hackmd import getcode
from overwrite import *
from variable import *

def checkpermission(update):
    chat_id = str(update.message.chat_id)
    developer_id = os.getenv("DEVELOPER_ID").split(',')
    if chat_id in developer_id:
        return True
    else:
        update.message.reply_text(
            "你沒有使用此指令的權限"
        )
        update.message.reply_text(
            "但名豐可以請客"
        )
        return False

# functions for commands
def backup(update, bot):
    if(not checkpermission(update)):   return

    code = getcode()
    
    fp2 = codecs.open("filename_back_up.txt", "w", "utf-8")
    fp2.write(code)
    fp2.close()

    update.message.reply_text(
        "手動備份完成"
    )

def undo(update, bot):
    if(not checkpermission(update)):   return

    update.message.reply_text(
        "還原中..."
    )
    
    overwrite('filename_auto_back_up.txt')

    update.message.reply_text(
        "以自動備份檔還原完成"
    )

def restore(update, bot):
    if(not checkpermission(update)):   return

    update.message.reply_text(
        "還原中..."
    )

    overwrite('filename_back_up.txt')

    update.message.reply_text(
        "以手動備份檔還原完成"
    )

def xhelp(update, bot):
    if(not checkpermission(update)):   return

    update.message.reply_text(
        'The followings are some commands: \n'
        '/xhelpzh : 查看中文管理員指令說明\n'
        '/xhelp : get this document.\n'
        '/clear : (debug tool) reset all variable about chat id.\n'
        '/backup : manually backup a hackmd data.\n'
        '/undo : overwrite hackmd data with auto_backup data.\n'
        '/restore : overwrite hackmd data with manual_backup data.\n'
        '/addtypo correct_text wrong_text : stronger search function.\n'
    )

def xhelpzh(update, bot):
    if(not checkpermission(update)):   return

    update.message.reply_text(
        '以下是管理員指令: \n'
        '/xhelpzh : 查看此說明\n'
        '/xhelp : get English document for administrator\'s commands\n'
        '/clear : (除錯工具) 重置關於此 chat_id 的所有狀態\n'
        '/backup : 手動備份資料。\n'
        '/undo : 從上次的自動備份還原菜單。\n'
        '/restore : 從上次的手動備份還原菜單。\n'
        '/addtypo 正確詞 錯誤詞 : 新增常見錯字資料。\n'
    )


def clearallrequest(update, bot):
    if(not checkpermission(update)):   return

    chat_id = str(update.message.chat_id)

    if(chat_id in status):
        del(status[chat_id])

    if(chat_id in add_query_shopname):
        del(add_query_shopname[chat_id])

    if(chat_id in add_query_classification):
        del(add_query_classification[chat_id])

    if(chat_id in add_query_photolink):
        del(add_query_photolink[chat_id])
    
    update.message.reply_text(
        "已清除您的所有要求"
    )
    print('status', status)

def addtypo(update, bot):
    if(not checkpermission(update)):   return

    chat_id = str(update.message.chat_id)
    correct, wrong = update.message.text[len('/addtypo '):].split()
    
    fp = codecs.open("typo.json", "r", "utf-8")
    r = json.load(fp)
    fp.close()

    if correct in r:
        r[correct].append(wrong)
    else:
        r[correct] = [wrong]
    r = str(r)
    r = r.replace("\'", "\"")

    fp = codecs.open("typo.json", "w", "utf-8")
    fp.write(str(r))
    fp.close()
    
    update.message.reply_text(
        "已新增"
    )

    # for key in r:
    #     for typo in r[key]:
    #         while(typo in text):
    #             index = text.index(typo)
    #             lens = len(typo)
    #             text = text[0:index] + key + text[(index+lens):]


def test(update, bot):
    if(not checkpermission(update)):   return

    chat_id = str(update.message.chat_id)
    update.send_message(chat_id, "hihi")