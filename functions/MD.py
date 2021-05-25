import platform, os
from functions.fileRW import *

classMap = {'宵夜街':2, '後門':3, '奢侈街':4, '山下':5, '校內':6}
classLen = len(classMap.keys())
anti_classMap = {}
for key in classMap.keys():
    anti_classMap[classMap[key]] = key

class MD:
    # 建構式
    def __init__(self, filename='filename.txt'):
        self.filename = filename
        self.pull()

    '''
    self.text
    self.title
    self.index
    self.menus
    self.shops
    self.images
    '''

    # private functions
    def pull(self):
        self.text = Concat_Lines(read(self.filename))
        
        tmp = self.text.split('\n## ')
        for i in range(1, len(tmp)):
            tmp[i] = '## ' + tmp[i]
        self.title = tmp[0]
        self.index = tmp[1]
        self.menus = tmp[2:]

        self.shops = []
    

        for i in classMap.keys():
            self.shops.append(self.menus[classMap[i]-2].split('\n### ')[1:])

        for i in range(len(self.shops)):
            for j in range(len(self.shops[i])):
                self.shops[i][j] = self.shops[i][j].split('\n')[0]
        
        


        self.images = []
        for i in range(len(classMap.keys())):
            self.images.append({})

        for i in range(len(self.shops)):
            curMenu = self.menus[i].split('\n### ')[1:]


            for j in range(len(curMenu)):
                curShopMenu = curMenu[j].split('\n')[:-1]
                curShopName = curShopMenu[0]
                if '`' in curShopMenu[-1]:
                    curShopUrl = curShopMenu[1:-1]
                    curShopTag = curShopMenu[-1].split(' ')[:-1]
                else:
                    curShopUrl = curShopMenu[1:]
                    curShopTag = []

                for k in range(len(curShopUrl)):
                    curShopUrl[k] = curShopUrl[k].split('![](')[1].split(' =400x)')[0]

                self.images[i].update({curShopName:[curShopUrl, curShopTag]})
            
    def reload(self):
        self.pull()

    def updateIndex(self):
        maximum = -1
        for i in self.shops:
            maximum = max(maximum, len(i))

        ret = '## 索引\n|'
        for i in classMap.keys():
            ret+=i + '|'
        ret += '\n|'
        for i in classMap.keys():
            ret+=':---:|'

        for i in range(maximum):
            ret+='\n|'
            for j in classMap.keys():
                if i<len(self.shops[classMap[j]-2]):
                    ret += '[{}](##{})|'.format(self.shops[classMap[j]-2][i], self.shops[classMap[j]-2][i])
                else:
                    ret += '|'
        ret+='\n\n'
            
        self.index = ret

    def updateMenus(self):
        retList = []
        for i in classMap.keys():
            ret = '## {}\n'.format(i)
            for j in self.images[classMap[i]-2].keys():
                ret += '### {}\n'.format(j)
                for k in self.images[classMap[i]-2][j][0]:
                    ret += '![]({} =400x)\n'.format(k)
                for k in self.images[classMap[i]-2][j][1]:
                    ret += '{} '.format(k)
                if len(self.images[classMap[i]-2][j][1])>0:    
                    ret += '\n'
                ret += '\n'
            retList.append(ret[:-1])
        
        self.menus = retList

    def updateText(self):
        ret = self.title + '\n' + self.index + '\n'
        # print(self.menus)
        # print('-------')
        for i in self.menus:
            ret += i + '\n'
        self.text = ret[:-1]

    def push(self, local = False, auto = False, manual = False, hackmd = False, admin = False):
        if local:
            write(self.filename, self.text)
        if auto:
            write('filename_auto_back_up.txt', self.text)
        if manual:
            write('filename_back_up.txt', self.text)
        if hackmd:
            print('overwritting,', platform.system())
            if platform.system() == 'Windows':
                command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' ' + self.filename
            else:
                command = "modules/hackmd-overwriter/bin/overwrite " + os.getenv("MD_SOURCE") + ' ' + self.filename
            print(command)
            os.system(command)

        if admin:
            pass


    def backup(self):
        pass

    def restore(self):
        pass
    
    
    # Shop:
    def getshops(self):
        return self.shops

    def getshops(self):   # return a list including all shops
        return self.shops

    # Menu:
    def editMenu(self, category, shopname, newMenus, newtag=[], updateNow = True, pushNow = False):
        self.images[classMap[category]-2].update({shopname: [newMenus, newtag] })
        if updateNow:
            self.updateMenus()
            self.updateText()
            if pushNow:
                self.push(local=True)
        print(self.text)
        pass        
    
    def getMenu(self, shopname):  # return a list including all links to shopname
        for i in self.images:
            if shopname in i:
                return i[shopname][0]
        return []

    # Tag: 
    def getTag(self, shopname): # retun list of tags to a shop
        for i in self.images:
            if shopname in i:
                return i[shopname][1]
        return []    
    

    def editTag(self, shopname, tags):  # no return now
        write('filename_auto_back_up.txt', self.text)
        classification = ''
        for i in range(len(self.shops)):
            if shopname in self.shops[i]:
                classification = anti_classMap[i+2]
        if classification !='':
            self.editMenu(classification, shopname, self.getMenu(shopname), newtag=tags, pushNow=True)

    # about more than two variable: 
    def add(self, category, shopname, menus=[], tag=[], updateNow = True, pushNow = False):
        self.shops[classMap[category]-2].append(shopname)
        self.images[classMap[category]-2].update({shopname:[menus, tag]})
        if updateNow:
            self.updateIndex()
            self.updateMenus()
            self.updateText()
            if pushNow:
                self.push(local=True)
    
    def editName(self, category, oldName, newName, updateNow = True, pushNow = False):
        for i in range(len(self.shops[classMap[category]-2])):
            if self.shops[classMap[category]-2][i] == oldName:
                self.shops[classMap[category]-2][i] = newName
                break
        curMenus = self.images[classMap[category]-2].get(oldName)
        self.images[classMap[category]-2].update({newName: curMenus })
        del self.images[classMap[category]-2][oldName]
        if updateNow:
            self.updateIndex()
            self.updateMenus()
            self.updateText()
            if pushNow:
                self.push(local=True)
        print(self.text)
    
    def delete(self, category, shopname, updateNow = True, pushNow = False):
        self.shops[classMap[category]-2].remove(shopname)
        del self.images[classMap[category]-2][shopname]
        if updateNow:
            self.updateIndex()
            self.updateMenus()

            self.updateText()
            if pushNow:
                self.push(local=True)
    


    # Other: 
    def getCategory(self, shopname):
        for i in range(len(self.shops)):
            if shopname in self.shops[i]:
                return anti_classMap[i+2]
        return None
