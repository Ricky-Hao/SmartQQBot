# coding:utf-8
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils

plugins_name="Wiki"
HELP={
    1:'Wiki: 维基百科插件',
    2:'Wiki 关键词: 自动检索维基百科对应关键词的简介',
    3:'百科 关键词: 自动检索维基百科对应关键词的简介'
}
proxies={"https":"socks5://127.0.0.1:1080"}
params={"action":"opensearch",'search':'','namespace':'0'}
p={'action':'query','list':'search','format':'json','srsearch':''}
url="https://zh.wikipedia.org/w/api.php"

@on_all_message(name=plugins_name)
def Wiki(msg,bot):
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugins_name):
        if utils.is_match('^(百科|Wiki|wiki) (.*)$',msg.content):
            p['srsearch']=utils.is_match('^(百科|Wiki|wiki) (.*)$',msg.content).group(2)
            tmp=requests.get(url,p,proxies=proxies)
            try:
                params['search']=json.loads(tmp.text)['query']['search'][0]['title']
            except:
                params['search']=p['srsearch']
            logger.info('[Wiki] Searching: '+params['search']+' for '+account_type+': '+account)
            tmp=requests.get(url,params=params,proxies=proxies)
            if tmp.status_code==200:
                try:
                    result=json.loads(tmp.text)[2][0]
                    if result!='':
                        bot.reply_msg(msg,result)
                    else:
                        bot.reply_msg(msg,'未找到相关信息哦~')
                except Exception as e:
                    logger.debug(e)
            else:
                bot.reply_msg(msg,"网络出错了哦~")
                
