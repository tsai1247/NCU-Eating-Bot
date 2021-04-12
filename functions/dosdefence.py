from variable import dos_defence, penalty, dos_maximum

def isDos(update):
    chat_id = getID(update)
    date = update.message.date

    if chat_id not in dos_defence:
        dos_defence[chat_id] = [1, date]
        return False
        
    count = dos_defence[chat_id][0]
    lasttime = dos_defence[chat_id][1]
    during = (date-lasttime).total_seconds()

    if count==-1:
        if during>penalty:
            dos_defence.update({chat_id : [1, date]})
            return False
        else:
            dos_defence.update({chat_id : [-1, date]})
            return True
    elif during>60:
        dos_defence.update({chat_id : [1, date]})
        return False
    elif count<dos_maximum:
        dos_defence.update({chat_id : [count+1, date]})
        return False
    else:
        dos_defence.update({chat_id : [-1, date]})
        return True

def getID(update):
    return str(update.message.from_user.id)