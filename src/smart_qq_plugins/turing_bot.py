# coding: utf-8
from random import randint
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import sqlite3
import base64

# 使用前请先前往 http://apistore.baidu.com/apiworks/servicedetail/736.html
# 申请 API 谢谢
# 另外需要 requests 支持
url = "http://apis.baidu.com/turing/turing/turing"
with open("./config/baidu_api_key.conf","r") as f:
    headers = {
        'apikey': f.read().strip('\n')
    }

con = sqlite3.connect("./config/data.db")
cur=con.cursor()
cur.execute('select uin from uin_plugins where plugin_name="turing_bot";')
a=cur.fetchall()
uin=[]
for i in a:
    uin.append(i[0])
cur.close()
con.close()


@on_all_message(name='turing_bot')
def turing_robot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """
    if str(msg.from_uin) in uin:
        con = sqlite3.connect("./config/data.db")
        cur=con.cursor()
        cur.execute('select nickname from basic where uin="{0}";'.format(str(msg.from_uin)))
        nickname=cur.fetchall()[0][0]
        cur.close()
        con.close()
        with open("./config/turing_api_key.conf","r") as f:
            querystring = {
                "key": f.read().strip('\n'),
                "info": msg.content.strip(nickname+"，"),
                "userid": base64.b64encode(nickname.encode())
            }
        with open("./config/group_code.json","r") as f:
            group_code=json.load(f)

        if msg.content.rfind(nickname+"，")==0:
            response = requests.get(url,headers=headers,params=querystring)
            response_json = response.json()
            bot.reply_msg(msg, response_json.get('text').strip("亲爱的，"))
