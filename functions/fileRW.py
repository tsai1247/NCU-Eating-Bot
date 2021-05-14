import codecs, json
import threading

lock_filename = threading.Lock()

def read(filename):
    lock_filename.acquire()
    if '.json' in filename:
        fp = codecs.open(filename, "r", "utf-8")
        ret = json.load(fp)
        fp.close()
    else:
        fp = codecs.open(filename, "r", "utf-8")
        ret = fp.readlines()
        fp.close()
        
    lock_filename.release()
    return ret

def write(filename, data):
    lock_filename.acquire()
    fp2 = codecs.open(filename, "w", "utf-8")
    fp2.write(data)
    fp2.close()
    lock_filename.release()

def append(filename, data):
    lock_filename.acquire()
    fp2 = codecs.open(filename, "a", "utf-8")
    fp2.write(data)
    fp2.close()
    lock_filename.release()

def Concat_Lines(lines):
    return ''.join(lines)