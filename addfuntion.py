import codecs, os
from functions.fileRW import Concat_Lines, read, write, append

# get input
dic = -1

while dic<1 or dic>4:
    try:
        dic = int(input('1. all_thread_admin\n' +
                        '2. all_thread_protectedcommand\n' +
                        '3. all_thread_command\n' +
                        '4. functions\n' +
                        '>> ').split('.')[0])
    except ValueError:
        dic = -1

if dic<4:
        command_name = input(   'Command name(/defaultname):\n' +
                                '>> ')
        try:
            command_name = command_name.split('/')[1]
        except IndexError:
            command_name = command_name.split('/')[0]

function_name = input(  'Function name:\n' +
                        '>> ')


# fileRW
if dic==1: # admin
    write('all_thread_admin/{}.py'.format(function_name), (
        '#!/usr/bin/env python3\n' + 
        '# coding=UTF-8\n' +
        'from functions.checkpermission import checkpermission\n' +
        'from functions.appendlog import appendlog\n' +
        'from functions.dosdefence import getID, isDos\n' +
        'import threading\n' +
        '\n' + 
        'class thread_{}(threading.Thread):\n'.format(function_name) +
        '\tdef __init__(self, update, bot):\n' +
        '\t\tthreading.Thread.__init__(self)\n' +
        '\t\tself.update = update\n' +
        '\t\tself.bot = bot\n' +
        '\t\t\n' +
        '\tdef run(self):\n' +
        '\t\tupdate = self.update\n' +
        '\t\tbot = self.bot\n' +
                '\n' +
        '\t\tif isDos(update): return\n' +
        '\t\tif(not checkpermission(update)):   return\n' +
        '\t\t\n' +
        '\t\t# TODO: what the function do.\n' +
        '\t\t\n' +
        '\t\tappendlog(getID(update), update.message.from_user.full_name, update.message.text)\n'
    ))

    append('all_thread_admin/{}.py'.format('importall'), '\nfrom all_thread_admin.{} import *'.format(function_name))

    append('admin.py', (
        '\n' + 
        'def {}(update, bot):\n'.format(function_name) +
        '\tthread_{}(update, bot).start()\n'.format(function_name)
    ))


    code = Concat_Lines(read('main.py'))
    code = code.split('# normal messages')
    code[0] = code[0][:-6]
    code[0] = code[0] + ('    updater.dispatcher.add_handler(CommandHandler(\'{}\', {}))\n\n    '.format(command_name, function_name))
    write('main.py', '# normal messages'.join(code))

    os.system('start ./all_thread_admin/{}.py'.format(function_name))

elif dic==2: # lower permission
    
    write('all_thread_protectedCommand/{}.py'.format(function_name), (
        '#!/usr/bin/env python3\n' + 
        '# coding=UTF-8\n' +
        'from functions.checkpermission import checkpermission, checkLowerPermission\n' +
        'from functions.appendlog import appendlog\n' +
        'from functions.dosdefence import getID, isDos\n' +
        'import threading\n' +
        '\n' + 
        'class thread_{}(threading.Thread):\n'.format(function_name) +
        '\tdef __init__(self, update, bot):\n' +
        '\t\tthreading.Thread.__init__(self)\n' +
        '\t\tself.update = update\n' +
        '\t\tself.bot = bot\n' +
        '\t\t\n' +
        '\tdef run(self):\n' +
        '\t\tupdate = self.update\n' +
        '\t\tbot = self.bot\n' +
                '\n' +
        '\t\tif isDos(update): return\n' +
        '\t\tif(not checkpermission(update)):   return\n' +
        '\t\tif(not checkLowerPermission(update)):   return\n' +
        '\t\t\n' +
        '\t\t# TODO: what the function do.\n' +
        '\t\t\n' +
        '\t\tappendlog(getID(update), update.message.from_user.full_name, update.message.text)\n'
    ))

    append('all_thread_protectedCommand/{}.py'.format('importall'), '\nfrom all_thread_protectedCommand.{} import *'.format(function_name))

    append('protectedCommand.py', (
        '\n' + 
        'def {}(update, bot):\n'.format(function_name) +
        '\tthread_{}(update, bot).start()\n'.format(function_name)
    ))


    code = Concat_Lines(read('main.py'))
    code = code.split('# all_thread_admin')
    code[0] = code[0][:-6]
    code[0] = code[0] + ('    updater.dispatcher.add_handler(CommandHandler(\'{}\', {}))\n\n    '.format(command_name, function_name))
    write('main.py', '# all_thread_admin'.join(code))

    os.system('start ./all_thread_protectedCommand/{}.py'.format(function_name))


elif dic==3: # normal command
    
    write('all_thread_command/{}.py'.format(function_name), (
        '#!/usr/bin/env python3\n' + 
        '# coding=UTF-8\n' +
        'from functions.appendlog import appendlog\n' +
        'from functions.dosdefence import getID, isDos\n' +
        'import threading\n' +
        '\n' + 
        'class thread_{}(threading.Thread):\n'.format(function_name) +
        '\tdef __init__(self, update, bot):\n' +
        '\t\tthreading.Thread.__init__(self)\n' +
        '\t\tself.update = update\n' +
        '\t\tself.bot = bot\n' +
        '\t\t\n' +
        '\tdef run(self):\n' +
        '\t\tupdate = self.update\n' +
        '\t\tbot = self.bot\n' +
                '\n' +
        '\t\tif isDos(update): return\n' +
        '\t\t\n' +
        '\t\t# TODO: what the function do.\n' +
        '\t\t\n' +
        '\t\tappendlog(getID(update), update.message.from_user.full_name, update.message.text)\n'
    ))

    append('all_thread_command/{}.py'.format('importall'), '\nfrom all_thread_command.{} import *'.format(function_name))

    append('command.py', (
        '\n' + 
        'def {}(update, bot):\n'.format(function_name) +
        '\tthread_{}(update, bot).start()\n'.format(function_name)
    ))


    code = Concat_Lines(read('main.py'))
    code = code.split('# all_thread_protectedcommand')
    code[0] = code[0][:-6]
    code[0] = code[0] + ('    updater.dispatcher.add_handler(CommandHandler(\'{}\', {}))\n\n    '.format(command_name, function_name))
    write('main.py', '# all_thread_protectedcommand'.join(code))

    os.system('start ./all_thread_command/{}.py'.format(function_name))

elif dic==4: # normal function
    write('functions/{}.py'.format(function_name), '\ndef {}():\n\tpass\n'.format(function_name))
    os.system('start ./functions/{}.py'.format(function_name))