import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils

plugin_name='Echo'

@on_all_message(name=plugin_name)
def Echo(msg,bot):
    