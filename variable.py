#!/usr/bin/env python3
# coding=UTF-8
import os
from dotenv import load_dotenv

load_dotenv() # Loading environment variable from .env file

url = os.getenv("MD_SOURCE")
status = {}
add_query_classification = {}
add_query_shopname = {}
add_query_update = {}
add_query_photolink = {}
classMap = {'宵夜街':2, '後門':3, '奢侈街':4, '山下':5}

dos_maximum = 25
penalty = 300
dos_defence= {}