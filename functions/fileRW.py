import codecs, json

def read(filename):
    if '.json' in filename:
        fp = codecs.open(filename, "r", "utf-8")
        ret = json.load(fp)
        fp.close()
    else:
        fp = codecs.open(filename, "r", "utf-8")
        ret = fp.readlines()
        fp.close()    
    return ret

def write(filename, data):
    fp2 = codecs.open(filename, "w", "utf-8")
    fp2.write(data)
    fp2.close()

def append(filename, data):
    fp2 = codecs.open(filename, "a", "utf-8")
    fp2.write(data)
    fp2.close()

def Concat_Lines(lines):
    ret = ''
    for line in lines:
        ret += line
    return ret