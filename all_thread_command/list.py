from fileRW import read
from telegram import ParseMode
from interact_with_hackmd import getlist
from appendlog import appendlog
from dosdefence import getID, isDos
from variable import *
import threading


def preprocess(text):
    ignorespace = ''
    for i in text:
        if i not in ignore_list:
            ignorespace+=i
    text = ignorespace
    r = read('typo.json')
    for key in r:
        for typo in r[key]:
            text = text.replace(typo, key)

    return text


class thread_list(threading.Thread):
    def __init__(self, update, bot):
        threading.Thread.__init__(self)
        self.update = update
        self.bot = bot
        
    def run(self):
        update = self.update
        bot = self.bot
        
        if isDos(update): return

        list = getlist().split('|')
        newlist = []
        for j in range(len(classMap.keys())):
            newlist.append([])
            for i in range((classLen+1)*2+1+j, len(list), len(classMap.keys())+1):
                if preprocess(list[i])!='':
                    newlist[j].append(list[i].split('[')[1].split(']')[0])
        
        for i in anti_classMap.keys():
            list = newlist[i-2]
            reply = '<b><i>' + anti_classMap[i] + '</i></b>：\n'
            count = 0
            max_word = 4
            single_line_cnt = 3
            
            for shop in list:
                reply += shop
                count += 1
                if count%single_line_cnt==0:
                    reply+='\n'
                elif len(shop)>max_word:
                    reply+='\n'
                    count = 0
                else:
                    for j in range(max_word-len(shop)+1):
                        reply += '\t\t\t\t'
            update.message.reply_text(reply, parse_mode=ParseMode.HTML)

        appendlog(getID(update), update.message.from_user.full_name, update.message.text)