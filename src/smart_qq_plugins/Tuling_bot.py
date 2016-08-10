# coding: utf-8
from random import randint
import requests
import re
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_private_message,on_group_message
import smart_qq_bot.sqlite as sql
import sqlite3
import base64

######
# 使用前请先前往 http://apistore.baidu.com/apiworks/servicedetail/736.html
# 申请 API 谢谢
# 另外需要 requests 支持
url = "http://apis.baidu.com/turing/turing/turing"
with open('./config/API_Key.json','r') as f:
    API_KEY=json.load(f)
headers = {
    'apikey': API_KEY.get('Baidu')
}
plugin_name='Tuling_bot'
######

######
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
######

######
update_id(plugin_name)
######


@on_group_message(name=plugin_name)
def Tuling_robot_group(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """
    update_id(plugin_name)
    gc=msg.group_id
    if in_group(gc):
        nickname=sql.fetch_one('select nickname from Nickname_group where group_id="{0}";'.format(gc))[0]
        if is_match('^'+nickname+'\W(.+)',msg.content):
            querystring = {
                "key": API_KEY.get('Tuling'),
                "info": is_match('^'+nickname+'\W(.+)',msg.content).group(1),
                "userid": base64.b64encode(nickname.encode())
            }

            if is_match('^'+nickname+'\W(.+)',msg.content):
                response = requests.get(url,headers=headers,params=querystring)
                response_json = response.json()
                bot.reply_msg(msg, response_json.get('text').strip("亲爱的，"))


@on_private_message(name=plugin_name)
def Tuling_robot_private(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """
    update_id(plugin_name)
    qq=msg.private_id
    if in_private(qq):
        nickname=sql.fetch_one('select nickname from Nickname_private where private_id="{0}";'.format(qq))[0]
        if is_match('^'+nickname+'\W.+',msg.content):
            querystring = {
                "key": API_KEY.get('Tuling'),
                "info": is_match('^'+nickname+'\W(.+)',msg.content).group(1),
                "userid": base64.b64encode(nickname.encode())
            }

            if is_match('^'+nickname+'\W(.+)',msg.content):
                response = requests.get(url,headers=headers,params=querystring)
                response_json = response.json()
                bot.reply_msg(msg, response_json.get('text').strip("亲爱的，"))