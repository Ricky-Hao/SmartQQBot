# coding:utf-8
import random
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import json
import sqlite3

REPLY_SUFFIX = (
    '~',
    '!',
    '?'
)
con = sqlite3.connect("./config/data.db")
cur=con.cursor()
cur.execute('select uin from uin_plugins where plugin_name="meow";')
a=cur.fetchall()
uin=[]
for i in a:
    uin.append(i[0])
cur.close()
con.close()

@on_all_message(name='meow')
def meow(msg,bot):
    if str(msg.from_uin) in uin:
        if "喵喵喵" in msg.content:
            logger.info('Meow to '+str(msg.group_code))
            bot.reply_msg(msg,"喵喵喵"+random.choice(REPLY_SUFFIX))
        '''elif "喵" in msg.content and "小喵" not in msg.content:
            logger.info('Meow to '+str(msg.group_code))
            bot.reply_msg(msg,"喵"+random.choice(REPLY_SUFFIX))'''
        return True
    return False
