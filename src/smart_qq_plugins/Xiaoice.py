# coding:utf-8
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
import itchat
import threading
from itchat.content import *

plugins_name="Xiaoice"
HELP={
    1:'Xiaoice: 微软小冰插件',
    2:'昵称+标点+想说的话'
}

last_msg=""
num=""
last_content=""
last_bot=""


class wechat(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        itchat.auto_login(hotReload=True,enableCmdQR=2)

    @itchat.msg_register(TEXT,isMpChat=True)
    def get_reply_from_xiaoice(msg):
        global last_msg
        global num
        global last_bot
        logger.info("[xiaoice] receive "+msg['Content'])
        if(msg['FromUserName']==num):
            last_bot.reply_msg(last_msg,msg['Content'])

    @itchat.msg_register(PICTURE,RECORDING,isMpChat=True)
    def repeat_if_no_text(msg):
        global last_content

        logger.info("[xiaoice] resend "+content)
        num=itchat.search_mps(name="小冰")[0]['UserName']
        itchat.send_msg(msg=last_content, toUserName=num)

    def run(self):
        itchat.run()

    @on_all_message(name=plugins_name)
    def xiaoice(msg,bot):
        global last_msg
        global num
        global last_bot
        global last_content
        (account,account_type)=utils.get_account_and_type(msg)
        if utils.in_plugins(account,account_type,plugins_name):
            nickname=sql.fetch_one('select nickname from Nickname where account="{0}" and account_type="{1}";'.format(account,account_type))[0]
            if account_type=='group' and utils.is_match('^'+nickname+'\W(.+)',msg.content):
                content=utils.is_match('^'+nickname+'\W(.+)',msg.content).group(1)
                logger.info("[xiaoice] send "+content)
                num=itchat.search_mps(name="小冰")[0]['UserName']
                itchat.send_msg(msg=content, toUserName=num)
                last_msg=msg
                last_bot=bot
                last_content=content
            elif account_type=='private' and utils.is_match('^([^!].*)$',msg.content):
                content=utils.is_match('^([^!].*)$',msg.content).group(1)
                logger.info("[xiaoice] send "+content)
                num=itchat.search_mps(name="小冰")[0]['UserName']
                itchat.send_msg(msg=content, toUserName=num)
                last_msg=msg
                last_bot=bot
                last_content=content

t=wechat()
t.start()
