# coding:utf-8
import random
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_group_message
import json

REPLY_SUFFIX = (
    '~',
    '!',
    '?'
)


@on_group_message(name='meow')
def meow(msg,bot):
    with open("./config/group_code.json","r") as f:
        group_code=json.load(f)
    if str(msg.group_code) in group_code.values():
        if "喵喵喵" in msg.content:
            logger.info('Meow to '+str(msg.group_code))
            bot.reply_msg(msg,"喵喵喵"+random.choice(REPLY_SUFFIX))
        elif "喵" in msg.content and "小喵" not in msg.content:
            logger.info('Meow to '+str(msg.group_code))
            bot.reply_msg(msg,"喵"+random.choice(REPLY_SUFFIX))
        return True
    return False
