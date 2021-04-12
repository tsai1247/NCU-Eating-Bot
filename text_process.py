from variable import ignore_list
from fileRW import read

def allin(small, big):
    for c in small:
        if(not c in big):   return False
    return True

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
