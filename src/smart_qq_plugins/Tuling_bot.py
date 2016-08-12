# coding: utf-8
from random import randint
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
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

######

######

######


@on_all_message(name=plugin_name)
def Tuling_robot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugin_name):
        nickname=sql.fetch_one('select nickname from Nickname where account="{0}" and account_type="{1}";'.format(account,account_type))[0]
        if utils.is_match('^'+nickname+'\W(.+)',msg.content):
            querystring = {
                "key": API_KEY.get('Tuling'),
                "info": utils.is_match('^'+nickname+'\W(.+)',msg.content).group(1),
                "userid": base64.b64encode(nickname.encode())
            }
            response = requests.get(url,headers=headers,params=querystring)
            response_json = response.json()
            bot.reply_msg(msg, response_json.get('text').strip("亲爱的，"))
