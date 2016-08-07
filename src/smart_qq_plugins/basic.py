# -*- coding: utf-8 -*-
import random
import sqlite3
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
)

# =====唤出插件=====

# 机器人连续回复相同消息时可能会出现
# 服务器响应成功,但实际并没有发送成功的现象
# 所以尝试通过随机后缀来尽量避免这一问题
REPLY_SUFFIX = (
    '~',
    '!',
    '?',
    '||',
)
REPLY_CONTENT=(
    "干嘛（‘·д·）",
    "嗯",
    "肿么了",
    "在呀",
    "不约",
    "嗯哼",
    "啊哈"
)

con = sqlite3.connect("./config/data.db")
cur=con.cursor()
cur.execute('select uin from uin_plugins where plugin_name="basic";')
a=cur.fetchall()
uin=[]
for i in a:
    uin.append(i[0])
cur.close()
con.close()

@on_all_message(name='nickname')
def nickname(msg, bot):
    if str(msg.from_uin) in uin:
        if (msg.content.rfind("小浩")==0 and "小浩，" not in msg.content) or "有人吗" in msg.content:
            reply = bot.reply_msg(msg, return_function=True)
            logger.info("RUNTIMELOG " + str(msg.from_uin) + " calling me out, trying to reply....")
            reply_content = random.choice(REPLY_CONTENT) + random.choice(REPLY_SUFFIX)
            reply(reply_content)