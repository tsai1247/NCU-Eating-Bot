#!/usr/bin/env python3
# coding=UTF-8
from all_thread_protectedCommand.importall import *

def delete(update, bot):
    thread_delete(update, bot).start()

    
def edit(update, bot):
    thread_edit(update, bot).start()