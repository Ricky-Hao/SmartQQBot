# coding:utf-8
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils

plugins_name="Wiki"
proxies={"https":"socks5://127.0.0.1:1080"}
params={"action":"opensearch",'search':'','namespace':'0'}
url="https://zh.wikipedia.org/w/api.php"

@on_all_message(name=plugins_name)
def Wiki(msg,bot):
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugins_name):
        if utils.is_match('^(百科|Wiki) (.*)$',msg.content):
            params['search']=utils.is_match('^(百科|Wiki) (.*)$',msg.content).group(1)
            tmp=requests.get(url,params=params,proxies=proxies)
            if tmp.status_code==200:
                s=""
                try:
                    for i in tmp[2]:
                        s+=i+'\n'
                    bot.reply_msg(msg,s)
                except:
                    psss
            else:
                bot.reply_msg(msg,"网络出错了哦~")
                
