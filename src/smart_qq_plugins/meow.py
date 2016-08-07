from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import json

REPLY_SUFFIX = (
    '~',
    '!',
    '?'
)


@on_all_message(name='meow')
def meow(msg,bot):
    group_code=json.load(file("../config/group_code.json"))
    try:
        if msg.group_code in group_code.values():
            if "喵喵喵" in msg.content:
                try:
                    logger.info('Meow to ',msg.group_code)
                except:
                    pass
                bot.reply_msg(msg,"喵喵喵"+REPLY_SUFFIX)
            elif "喵" in msg.content:
                try:
                    logger.info('Meow to ',msg.group_code)
                except:
                    pass
                bot.reply_msg(msg,"喵"+REPLY_SUFFIX)
            return True
        return False
    except:
        pass
