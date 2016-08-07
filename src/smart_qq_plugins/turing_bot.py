# coding: utf-8
from random import randint
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_group_message

# 使用前请先前往 http://apistore.baidu.com/apiworks/servicedetail/736.html
# 申请 API 谢谢
# 另外需要 requests 支持
url = "http://apis.baidu.com/turing/turing/turing"
with open("./config/baidu_api_key.conf","r") as f:
    headers = {
        'apikey': f.read().strip('\n')
    }


@on_group_message
def turing_robot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """
    with open("./config/turing_api_key.conf","r") as f:
        querystring = {
            "key": f.read().strip('\n'),
            "info": msg.content.strip("小浩，"),
            "userid": "xiaohao"
        }
    with open("./config/group_code.json","r") as f:
        group_code=json.load(f)

    if str(msg.group_code) in group_code.values():
        if msg.content.rfind("小浩，")==0:
            response = requests.get(url,headers=headers,params=querystring)

            response_json = response.json()

            bot.reply_msg(msg, response_json.get('text').strip("亲爱的，"))
