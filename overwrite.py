import os

def overwrite(srcdata):
    command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' ' + srcdata
    os.system(command)