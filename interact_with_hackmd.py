import requests, codecs
from variable import *
from overwrite import *

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
    oldcode = fp.readlines
    print(oldcode)
    fp.close()

    fp2 = codecs.open("filename_auto_back_up.txt", "w", "utf-8")
    fp2.write(oldcode)
    fp2.close()

    fp = codecs.open("filename.txt", "w", "utf-8")
    fp.write(newcode)
    fp.close()

    overwrite('filename.txt')

def getcode():  # get all hackmd contents
  response = requests.get(url)
  sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
  code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
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
        # print(i)
        for j in range(len(i)):
        # print('>', j)
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
