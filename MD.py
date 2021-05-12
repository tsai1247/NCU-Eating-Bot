from functions.fileRW import *
from functions.variable import *

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
        self.text = ret

    def push(self):
        write(self.filename, self.text)

    def backup(self):
        pass

    def restore(self):
        pass

    # 方法(Method)
    def setfilename(self, filename='filename.txt'):
        self.filename = filename

    def getfilename(self):
        return self.filename

    def getshops(self):
        return self.shops

    def add(self, category, shopname, menus, updateNow = True, pushNow = False):
        self.shops[classMap[category]-2].append(shopname)
        self.images[classMap[category]-2].update({shopname:[menus, []]})
        if updateNow:
            self.updateIndex()
            self.updateMenus()
            self.updateText()
            if pushNow:
                self.push()
    
    def delete(self, category, shopname, updateNow = True, pushNow = False):
        self.shops[classMap[category]-2].remove(shopname)
        del self.images[classMap[category]-2][shopname]
        if updateNow:
            self.updateIndex()
            self.updateMenus()

            self.updateText()
            if pushNow:
                self.push()
    
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
                self.push()
        print(self.text)
    
    def editMenu(self, category, shopname, newMenus, updateNow = True, pushNow = False):
        self.images[classMap[category]-2].update({shopname: [newMenus, []] })
        if updateNow:
            self.updateMenus()
            self.updateText()
            if pushNow:
                self.push()
        print(self.text)
        pass
    