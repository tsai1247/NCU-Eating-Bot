import os

def overwrite(srcdata):
    command = "modules/hackmd-overwriter/bin/hackmd-overwriter " + os.getenv("MD_SOURCE") + ' ' + srcdata
    os.system(command)