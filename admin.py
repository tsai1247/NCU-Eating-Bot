from interact_with_hackmd import getcode
from overwrite import *
from variable import *
from dosdefence import *
from fileRW import *
from code_compare import *


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

    write("filename_back_up.txt", getcode())
    update.message.reply_text(
        "手動備份完成"
    )
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def undo(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    update.message.reply_text("還原中...")
    overwrite('filename_auto_back_up.txt')
    curData = Concat_Lines(read('filename.txt'))
    write('filename.txt', Concat_Lines(read('filename_auto_back_up.txt')))
    write('filename_auto_back_up.txt', curData)

    update.message.reply_text("以自動備份檔還原完成")

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def restore(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    update.message.reply_text("還原中...")
    overwrite('filename_back_up.txt')    
    curData = Concat_Lines(read('filename.txt'))
    write('filename.txt', Concat_Lines(read('filename_back_up.txt')))
    write('filename_auto_back_up.txt', curData)




    update.message.reply_text("以手動備份檔還原完成")

    write('filename.txt', Concat_Lines(read('filename_back_up.txt')))

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def xhelp(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    update.message.reply_text(xhelp_en)
    
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def xhelpzh(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    update.message.reply_text(xhelp_zh)

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)



def addtypo(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    correct, wrong = update.message.text[len('/addtypo '):].split()
    r = read("typo.json")
    if correct in r:    r[correct].append(wrong)
    else:   r[correct] = [wrong]
    r = str(r)
    r = r.replace("\'", "\"")
    write("typo.json", r)
    update.message.reply_text("已新增")

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def test(bot, update):
    if isDos(update): return
    if(not checkpermission(update)):   return
    
    print('hi')
    chat_id = getID(update)
    text = 'hihi~~'    
    # bot.send_message(chat_id, text)
    update.message.reply_text(update.toString())
    # appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def singleReport(update, num):
    if num==1:
        report_files = read('user_report.txt')
        update.message.reply_text('User Report:')
        for i in range(int(len(report_files)/30)):
            update.message.reply_text(Concat_Lines(report_files[i*30:(i+1)*30]))
        if len(report_files)>0:
            update.message.reply_text(Concat_Lines(report_files[int(len(report_files)/30)*30:]))
    elif num==2:
        shop_files = read('non-exist-shop.txt')
        update.message.reply_text('Non exist shops:')
        for i in range(int(len(shop_files)/30)):
            update.message.reply_text(Concat_Lines(shop_files[i*30:(i+1)*30]))
        if len(shop_files)>0:
            update.message.reply_text(Concat_Lines(shop_files[int(len(shop_files)/30)*30:]))
    elif num==3:
        logger_files = read('logger.txt')
        update.message.reply_text('Logger:')
        for i in range(int(len(logger_files) /30)):
            update.message.reply_text(Concat_Lines(logger_files[i*30:(i+1)*30]))
        if len(logger_files)>0:
            update.message.reply_text(Concat_Lines(logger_files[int(len(logger_files)/30)*30:]))
    else:
        update.message.reply_text('type error.')

def getreport(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    chat_id = getID(update)
   
    text = update.message.text.split()
    if len(text)>2:
        update.message.reply_text('type error.')
    elif len(text) == 2:
        if not text[1].isdecimal():
            update.message.reply_text('type error.')
        else:
            singleReport(update, int(text[1]))
    else:
       for i in range(1,4):
            singleReport(update, i)
    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def manual_overwrite(update, bot):
    if isDos(update): return
    if(not checkpermission(update)):   return

    textlist = update.message.text.split()
    if len(textlist)==1:    # /overwrite
        textlist.append('filename.txt')
        textlist.append('1')
    elif len(textlist)==2:    # /overwrite filename  | /overwrite num
        if textlist[1].isnumeric():     # /overwrite num
            textlist.append(textlist[1])
            textlist[1] = 'filename.txt'
        else:
            if '.' not in textlist[1]:    # /overwrite filename
                textlist[1] += '.txt'
            textlist.append('1')
    elif len(textlist)==3:    # /overwrite filename num
        if '.' not in textlist[1]:    # /overwrite filename
            textlist[1] += '.txt'
            
    else:
        update.message.reply_text('格式錯誤，請輸入 /overwrite 檔案名稱=filename.txt 執行次數=1')
        return

    for i in range(int(textlist[2])):
        update.message.reply_text('try overwriting with {}, {} time(s).'.format(textlist[1], i+1))
        overwrite(textlist[1])
        if comapreCode():
            update.message.reply_text('上傳成功')
            break
        else:
            update.message.reply_text('上傳失敗')
            break

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

def getID(update):
    return str(update.message.from_user.id)

def appendlog(user_id, username, text):
    append('logger.txt', '{}({}): {}\n'.format(user_id, username, text))
