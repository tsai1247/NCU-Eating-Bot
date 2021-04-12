from code_compare import comapreCode
from overwrite import overwrite
from checkpermission import checkpermission
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading

class thread_overwrite(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
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