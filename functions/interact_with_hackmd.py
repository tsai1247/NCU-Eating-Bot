#!/usr/bin/env python3
# coding=UTF-8
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from functions.dosdefence import getID
from functions.code_compare import comapreCode, getSpecificCode
from functions.fileRW import *
import random
from functions.variable import *
from functions.overwrite import *
from functions.appendlog import appendlog
from functions.text_process import preprocess, allin

def Levenshtein(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)
    if str1_len==0: 
        return str2_len
    if str2_len==0: 
        return str1_len
    if str1==str2:
        return 0
    
    cost = 0 if str1[0] == str2[0] else 1

    a = Levenshtein(str1[1:str1_len], str2) + 1
    if a>5: return 5

    b = Levenshtein(str1, str2[1:str2_len]) + 1
    if b>5: return 5
    
    c = Levenshtein(str1[1:str1_len], str2[1:str2_len]) + cost
    if c>5: return 5
    
    return min(a, b, c)

def updateHackmd(chat_id, classification, shopname, photolink):
    def updateIndex(code, index):
        undealtlist = code.split('|')[1:]

        dealtlist = []
        for i in range(int(len(undealtlist)/(classLen+1))):
            dealtlist.append([])
            for j in range(classLen):
                dealtlist[-1].append(undealtlist[i*(classLen+1)+j])

        reverseMenu = GetReverseMenu(dealtlist)
        
        for i in range(len(reverseMenu[index])):
            if(reverseMenu[index][i]==''):
                reverseMenu[index][i]= '[{}](##{})'.format(shopname, shopname)
                break
            elif i+1==len(reverseMenu[index]):
                reverseMenu[index].append('[{}](##{})'.format(shopname, shopname))
                for j in range(classLen):
                    if(j!=index):
                        reverseMenu[j].append('')
        
        reverseMenu = GetReverseMenu(reverseMenu)
        
        ret = getMDtable(reverseMenu)
        ret = '## 索引\n' + ret
        return ret

    def updatePhoto(code):
        code += '### {}\n'.format(shopname)
        for i in photolink:
            code += '![]({} =400x)\n'.format(i)
        code += '\n'
        return code
    
    add_query_classification.pop(chat_id)
    add_query_shopname.pop(chat_id)
    if chat_id in add_query_photolink:
        add_query_photolink.pop(chat_id)

    code = split(getcode()) # len = 7
                            # 菜單 索引 宵夜街 後門 奢侈街 山下 校內
    index = classMap[classification]
    code[1] = updateIndex(code[1], index-2)
    code[index] = updatePhoto(code[index])
    
    newcode = Concat_Lines(code)
    oldcode = getSpecificCode('local')
    write('filename_auto_back_up.txt', oldcode)
    write('filename.txt', newcode)

    overwrite('filename.txt')


def getcode():  # get all hackmd contents
    if(not comapreCode()):
        appendlog("", "", "last update failed.")
    return getSpecificCode('local')

def getlist():  # return the table of "索引" on hackmd
    code = getcode()
    list = code.split('## 索引')[1].split('## 宵夜街')[0]
    return list

def getshops():   # return a list including all shops
    tmp = getlist().split('|')[classLen+2:]
    list = []
    for i in tmp:
        if(not isempty(i)):
            list.append(i.split('[')[1].split(']')[0])
    return list

def getMenu(shopname):  # return a list including all menus to shopname
    code = getcode()
    urls = code.split('### ' + shopname)[1].split('###')[0].split('![]')
    list = []
    for i in range(1, len(urls)):
        pic = urls[i].split('(')[1].split(' =400x)')[0]
        list.append(pic)
    return list

def GetReverseMenu(curMenu):
    midpath = []
    for i in range(len(curMenu[0])):
        midpath.append([])
    for i in curMenu:
        for j in range(len(i)):
            midpath[j].append(i[j])

    return midpath

def getMDtable(reverseMenu):
    ret = ''
    for i in reverseMenu:
        ret+='|'
        for j in i:
            ret+= j + '|'
        ret+='\n'

    return ret

def isempty(st):
    num = st.count(' ')+st.count('\n')+st.count(':')+st.count('-')
    return (num==len(st))

def split(code):
    ret = []

    ret.append(code.split('## 索引')[0])
    code = '## 索引' + code.split('## 索引')[1]

    for i in classMap.keys():
        sep = '## {}'.format(i)
        ret.append(code.split(sep)[0])
        code = sep + code.split(sep)[1]

    ret.append(code)
    return ret

def get_tags(shopname):
    code = split(getcode())[2:]
    list = []
    for i in code:
        if shopname in i:
            list = i.split('### ' + shopname)[1].split('###')[0].split('`')[1::2]
            break
    return list

def update_tag(shopname, tags):
    code = split(getcode())
    newcode = code[0] + code[1]
    for i in code[2:]:
        if shopname in i:
            side_shops = i.split('### ' + shopname)[0] + '### ' + shopname
            goalshop = i.split('### ' + shopname)[1]
            goalshop_begin = goalshop.split('###')[0][:-1].split('`')[0]
            for tag in tags:
                goalshop_begin += '`' + tag + '` '
            goalshop_begin += '\n\n'
            try:
                goalshop_ends = goalshop.split('###')[1:]
                goalshop_end = ''
                for i in goalshop_ends:
                    goalshop_end += '###' + i
            except IndexError:
                goalshop_end = ''

            newcode += side_shops + goalshop_begin + goalshop_end
        else:
            newcode += i
    oldcode = getSpecificCode('local')
    write('filename_auto_back_up.txt', oldcode)
    write('filename.txt', newcode)
    overwrite('filename.txt')
    return


def findmenu(text, update):
    text = preprocess(text)
    chat_id = getID(update)
    list = getshops()
    if text in list:
        curMenu = getMenu(text)
        for photolink in curMenu:
            update.message.reply_photo(photolink)
    else:
        candi_list = []
        print('keyword: {}'.format(text))
        for shop in list:
            if(allin(shop, text) or allin(text, shop) or Levenshtein(shop, text)<2):
                candi_list.append(shop)
        
        if(len(candi_list)>5):
            random.shuffle(candi_list)
            candi_list = candi_list[0:5]

        if(len(candi_list)==0):
            update.message.reply_text('此店家不存在')
            append('non-exist-shop.txt', '{}\n'.format(text))
        else:
            add_query_update.update({chat_id:update})        
            status.update({chat_id:'search_step1'})
            update.message.reply_text("我猜你想查",
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list[0::2]],
                    [InlineKeyboardButton(s, callback_data = '{} {} {}'.format(s, chat_id, 1)) for s in candi_list[1::2]]
                ]))

    appendlog(getID(update), update.message.from_user.full_name, update.message.text)

