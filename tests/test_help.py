#!/usr/bin/env python3
# coding=UTF-8
import os
import sys

from .client import client

sys.path.append(os.path.abspath(os.getcwd()))

from functions.variable import help_en, help_zh, xhelp_en, xhelp_zh

def test_help():
    client.send('@NCU_Eating_Bot', '/help')
    assert client.receive('@NCU_Eating_Bot')[0].text.strip() == help_en.strip()

def test_helpzh():
    client.send('@NCU_Eating_Bot', '/helpzh')
    assert client.receive('@NCU_Eating_Bot')[0].text.strip() == help_zh.strip()

def test_xhelp():
    client.send('@NCU_Eating_Bot', '/xhelp')
    assert client.receive('@NCU_Eating_Bot')[0].text.strip() == xhelp_en.strip()

def test_xhelpzh():
    client.send('@NCU_Eating_Bot', '/xhelpzh')
    assert client.receive('@NCU_Eating_Bot')[0].text.strip() == xhelp_zh.strip()
