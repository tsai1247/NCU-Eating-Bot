import codecs
from command import preprocess
import json, requests

from interact_with_hackmd import getcode
from overwrite import *
from variable import *
from dosdefence import *

def checkpermission(update):
    chat_id = getID(update)
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
    if isDos(update): return
    if(not checkpermission(update)):   return

    code = getcode()
    
    fp2 = codecs.open("filename_back_up.txt", "w", "utf-8")
    fp2.write(code)
    fp2.close()

    update.message.reply_text(
        "手動備份完成"
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def undo(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    update.message.reply_text(
        "還原中..."
    )
    
    overwrite('filename_auto_back_up.txt')

    update.message.reply_text(
        "以自動備份檔還原完成"
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def restore(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    update.message.reply_text(
        "還原中..."
    )

    overwrite('filename_back_up.txt')

    update.message.reply_text(
        "以手動備份檔還原完成"
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def xhelp(update, bot):
    if isDos(update): return
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
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
def xhelpzh(update, bot):
    if isDos(update): return
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
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)



def addtypo(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    chat_id = getID(update)
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
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def test(bot, update):
    if isDos(update): return
    if(not checkpermission(update)):   return
    
    print('hi')
    chat_id = getID(update)
    text = 'hihi~~'
    
    bot.send_message(chat_id, text)


    # appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def getreport(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    chat_id = getID(update)
    
    fp = codecs.open("user_report.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()

    report_files = ''
    for i in oldcode:
        report_files += i
    

    update.message.reply_text(
        'User Report:\n' + report_files
    )

    fp = codecs.open("non-exist-shop.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()

    report_files = ''
    for i in oldcode:
        report_files += i
    

    update.message.reply_text(
        'Unfind Shops:\n' + report_files
    )
    
    fp = codecs.open("logger.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()

    report_files = ''
    for i in oldcode:
        report_files += i
    

    update.message.reply_text(
        'logger:\n' + report_files
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)
    
def manual_overwrite(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    text = update.message.text
    text = preprocess(text.split('/overwrite')[1])
    if('@NCU_Eating_Bot' in text):
        text = text.split('@NCU_Eating_Bot')[1]
    
    try:
        num = int(text)
        for i in range(num):
            update.message.reply_text(
               'try overwrite with {}'.format(text)
            )
            overwrite('filename.txt')
            response = requests.get(url)
            sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
            code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
            fp = codecs.open("filename.txt", "r", "utf-8")
            oldcode = fp.readlines()
            fp.close()
            tmp = ''
            for i in oldcode:
                tmp+=i
            oldcode = tmp
            if code == oldcode:
                update.message.reply_text(
                    '上傳成功'
                )
                return
            elif i+1==num:
                update.message.reply_text(
                    '上傳失敗'
                )
                return
    except:
        if(text==''):
            text = 'filename.txt'
        if(not '.' in text):
            text += '.txt'
        update.message.reply_text(
            'try overwrite with {}'.format(text)
        )
    overwrite(text)

    response = requests.get(url)
    sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
    code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
    
    fp = codecs.open(text, "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()
    tmp = ''
    for i in oldcode:
        tmp+=i
    oldcode = tmp

    if(oldcode == code):
        update.message.reply_text(
            '上傳成功'
        )
    else:
        update.message.reply_text(
            '上傳失敗'
        )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def getID(update):
    return str(update.message.from_user.id)

def appendlog(user_id, username, text):
    fp2 = codecs.open("logger.txt", "a", "utf-8")
    fp2.write('{}({}): {}\n'.format(user_id, username, text))
    fp2.close()
