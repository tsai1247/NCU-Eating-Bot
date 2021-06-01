#!/usr/bin/env python3
# coding=UTF-8

import os
from time import sleep
from pyrogram import Client

class TelegramClient:

    def __init__(self):          

        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")  
        session = os.getenv("TG_SESSION")

        self.client = Client(session, api_id, api_hash)        
        self.client.start()
        self.wait = lambda : sleep(3)

    def send(self, chat_id , message):
        self.client.send_message(chat_id, message)

    def receive(self, chat_id):
        self.wait()
        return self.client.get_history(chat_id, limit=1)

client = TelegramClient()