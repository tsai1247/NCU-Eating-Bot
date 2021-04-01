#!/usr/bin/env python3
# coding=UTF-8
import requests, codecs
from variable import *
from overwrite import *

def Levenshtein(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)
    if str1_len==0: 
        return str2_len
    if str2_len==0: 
        return str1_len
    if str1==str2:
        return 0
    
    cost = 1 if str1[0] == str2[0] else 0

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
        for i in range(int(len(undealtlist)/5)):
            dealtlist.append([])
            for j in range(4):
                dealtlist[-1].append(undealtlist[i*5+j])

        reverseMenu = GetReverseMenu(dealtlist)
        
        for i in range(len(reverseMenu[index])):
            if(reverseMenu[index][i]==''):
                reverseMenu[index][i]= '[{}](##{})'.format(shopname, shopname)
                break
            elif i+1==len(reverseMenu[index]):
                reverseMenu[index].append('[{}](##{})'.format(shopname, shopname))
                for j in range(4):
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
    del(add_query_classification[chat_id])
    del(add_query_shopname[chat_id])
    del(add_query_photolink[chat_id])

    code = split(getcode()) # len = 6
                            # 菜單 索引 宵夜街 後門 奢侈街 山下
    index = classMap[classification]
    code[1] = updateIndex(code[1], index-2)
    code[index] = updatePhoto(code[index])
    newcode = ''
    for i in code:
        newcode += i
    
    fp = codecs.open("filename.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()

    fp2 = codecs.open("filename_auto_back_up.txt", "w", "utf-8")
    for i in oldcode:
        fp2.write(i)
    fp2.close()

    fp = codecs.open("filename.txt", "w", "utf-8")
    fp.write(newcode)
    fp.close()

    overwrite('filename.txt')


def getcode():  # get all hackmd contents    
    fp = codecs.open("filename.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()
    tmp = ''
    for i in oldcode:
        tmp+=i
    oldcode = tmp
    try:
        response = requests.get(url)
        sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
        code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
        if code != oldcode:
            appendlog("last update failed.")
            code = oldcode
    except TimeoutError:
        code = oldcode

    return code

def getlist():  # return the table of "索引" on hackmd
    code = getcode()
    list = code.split('## 索引')[1].split('## 宵夜街')[0]
    return list

def getshops():   # return a list including all shops
    tmp = getlist().split('|')[6:-1]
    list = []
    for i in tmp:
        if(not isempty(i)):
            list.append(i.split('[')[1].split(']')[0])
    return list

def getMenu(shopname):  # return a list including all menus to shopname
    code = getcode()
    urls = code.split('### ' + shopname)[1].split('###')[0].split('![]')
    lst = []
    for i in range(1, len(urls)):
        pic = urls[i].split('(')[1].split(' =400x)')[0]
        lst.append(pic)
    return lst

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
    tmp = code

    ret.append(tmp.split('## 索引')[0])
    tmp = '## 索引' + tmp.split('## 索引')[1]

    ret.append(tmp.split('## 宵夜街')[0])
    tmp = '## 宵夜街' + tmp.split('## 宵夜街')[1]

    ret.append(tmp.split('## 後門')[0])
    tmp = '## 後門' + tmp.split('## 後門')[1]

    ret.append(tmp.split('## 奢侈街')[0])
    tmp = '## 奢侈街' + tmp.split('## 奢侈街')[1]

    ret.append(tmp.split('## 山下')[0])
    tmp = '## 山下' + tmp.split('## 山下')[1]

    ret.append(tmp)
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
    list = []
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

    fp = codecs.open("filename.txt", "r", "utf-8")
    oldcode = fp.readlines()
    fp.close()

    fp2 = codecs.open("filename_auto_back_up.txt", "w", "utf-8")
    for i in oldcode:
        fp2.write(i)
    fp2.close()

    fp = codecs.open("filename.txt", "w", "utf-8")
    fp.write(newcode)
    fp.close()

    overwrite('filename.txt')
    return

def appendlog(text):
    fp2 = codecs.open("logger.txt", "a", "utf-8")
    fp2.write(text+'\n')
    fp2.close()
