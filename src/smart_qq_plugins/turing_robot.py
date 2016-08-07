# coding: utf-8
from random import randint
import requests

from smart_qq_bot.signals import on_group_message

# 使用前请先前往 http://apistore.baidu.com/apiworks/servicedetail/736.html
# 申请 API 谢谢
# 另外需要 requests 支持
url = "http://apis.baidu.com/turing/turing/turing"
headers = {
    'apikey': "",
    'cache-control': "no-cache"
}


@on_group_message
def turing_robot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """

    querystring = {
        "key": file("./config/baidu_api_key.conf").read(),
        "info": msg.content,
        "userid": ""
    }
    group_code=json.load(file("./config/group_code.json"))

    if str(msg.group_code) in group_code.values():
        if "小浩，" in msg.content:
            response = requests.request("GET", url, headers=headers, params=querystring)

            response_json = response.json()

            bot.reply_msg(msg, response_json.get('text'))
