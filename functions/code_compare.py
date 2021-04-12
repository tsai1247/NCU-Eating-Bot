import requests
from functions.variable import url
from functions.fileRW import *

def getSpecificCode(text):
    if text =='local':
        oldcode = Concat_Lines(read('filename.txt'))
        return oldcode
    elif text == 'online':
        response = requests.get(url)
        sourcecode_begin = '<div id="doc" class="markdown-body container-fluid" data-hard-breaks="true">'
        code = response.text.split(sourcecode_begin)[1].split('</div>')[0]
        return code
    else:
        return None

def comapreCode():
    return ( getSpecificCode('local') == getSpecificCode('online') )
        