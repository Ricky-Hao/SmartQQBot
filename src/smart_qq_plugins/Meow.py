# coding:utf-8
import random
import re
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_group_message,on_private_message
import smart_qq_bot.sqlite as sql 
import json
import sqlite3

#######################################
REPLY_SUFFIX = (
    '~',
    '!',
    '?'
)

plugin_name="Meow"
#######################################

#######################################
def update_id(name):
    global group_id
    global private_id
    
    private_id=sql.get_private_id(name)
    group_id=sql.get_group_id(name)

def in_group(gc):
    global group_id
    return gc in group_id

def in_private(qq):
    global private_id
    return qq in private_id

def is_match(p,s):
    return re.match(p,s)
######################################

######################################
update_id(plugin_name)
######################################

######################################

@on_group_message(name=plugin_name)
def Meow_group(msg,bot):
    update_id(plugin_name)
    gc=msg.group_id
    if in_group(gc) and is_match(r'^喵{1,}\W*$',msg.content):
        bot.reply_msg(msg,'喵'*random.randint(1,6)+random.choice(REPLY_SUFFIX))

@on_private_message(name=plugin_name)
def Meow_private(msg,bot):
    update_id(plugin_name)
    qq=msg.private_id
    if in_private(qq) and is_match(r'^喵{1,}\W*$',msg.content):
        bot.reply_msg(msg,'喵'*random.randint(1,6)+random.choice(REPLY_SUFFIX))
