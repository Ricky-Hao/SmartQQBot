# coding: utf-8
import random
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
HELP={
    1:'Tuling_bot: 图灵机器人插件',
    2:'使用方法: 机器人昵称+标点+对话内容可以触发对话'
}
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
                "userid": account
            }
            response = requests.get(url,headers=headers,params=querystring)
            response_json = response.json()
            reply=response_json.get('text')
            if utils.is_match('^亲，已帮您找到(.*)$',reply):
                opt=utils.is_match('^亲，已帮您找到(.*)$',reply).group(1)
                if opt=="航班信息":
                    bot.reply_msg(msg,response_json['url'])
                elif opt=="列车信息":
                    bot.reply_msg(msg,response_json['url'])
                elif opt=="菜谱信息":
                    content_list=random.choice(response_json['list'])
                    bot.reply_msg(msg,content_list['name']+'\n'+content_list['info']+'\n'+content_list['detailurl'])

                elif opt=="相关新闻":
                    content_list=random.choice(response_json['list'])
                    bot.reply_msg(msg,content_list['article']+'\n'+content_list['detailurl'])

            elif utils.is_match('^亲，已帮你找到图片$',reply):
                bot.reply_msg(msg,response_json['url'])
            else:
                bot.reply_msg(msg, reply.strip("亲爱的，"))
