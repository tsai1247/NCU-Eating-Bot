import os
import platform

def overwrite(srcdata):
    print('overwritting,', platform.system())
    command = ''
    if platform.system() == 'Windows':
        command = "modules\\hackmd-overwriter\\bin\\overwrite.cmd " + os.getenv("MD_SOURCE") + ' ' + srcdata
    else:
        command = "modules/hackmd-overwriter/bin/overwrite " + os.getenv("MD_SOURCE") + ' ' + srcdata
    print(command)
    os.system(command)