#!/usr/bin/env python3
# coding=UTF-8
from all_thread_command.importall import *

def startbot(update, bot):
    thread_start(update, bot).start()

def help(update, bot):
    thread_help(update, bot).start()

def helpzh(update, bot):
    thread_helpzh(update, bot).start()

def randomfunc(update, bot):
    thread_random(update, bot).start()

def add(update, bot):
    thread_add(update, bot).start()

def callback(update, bot):
    thread_callback(update, bot).start()

def search(update, bot):
    thread_search(update, bot).start()

def whengettext(update, bot):
    thread_text(update, bot).start()

def whengetphoto(update, bot):
    thread_photo(update, bot).start()

def hint(update, bot):
    thread_hint(update, bot).start()

def whengetfile(update, bot):
    thread_file(update, bot).start()

def addtag(update, bot):
    thread_addtag(update, bot).start()

def clearallrequest(update, bot):
    thread_clear(update, bot).start()

def listall(update, bot):
    thread_list(update, bot).start()

def report(update, bot):
    thread_report(update, bot).start()
