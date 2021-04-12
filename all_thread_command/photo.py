from functions.appendlog import appendlog
from functions.dosdefence import getID, isDos
import threading

class thread_photo(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return
        update.message.reply_text('為確保資料完整性，請上傳未壓縮照片( /hint )。')
        update.message.reply_text('店家無菜單或傳送完畢請輸入 /add 結束傳送。')
        # DealWithPhotolink(update, update.message.photo[0].file_id)
        appendlog(getID(update), update.message.from_user.full_name, 'getphoto')