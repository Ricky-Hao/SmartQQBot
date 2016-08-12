# coding:utf-8
import random
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql 
import smart_qq_bot.utils as utils

#######################################
REPLY_SUFFIX = (
    '~',
    '!',
    '?'
)

plugin_name="Meow"
#######################################

#######################################

######################################

######################################

######################################

######################################

@on_all_message(name=plugin_name)
def Meow(msg,bot):
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugin_name) and utils.is_match(r'^喵{1,}\W*$',msg.content):
        bot.reply_msg(msg,'喵'*random.randint(1,6)+random.choice(REPLY_SUFFIX))
