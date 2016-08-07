import requests
import re

from smart_qq_bot.logger import logger
from smart_qq_bot.messages import GroupMsg
from smart_qq_bot.signals import on_group_message, on_bot_inited

@on_group_message(name="163music")
def searchmusic(msg,bot):
    match = re.match(ur'^(music|音乐) (\w+|[\u4e00-\u9fa5]+)', msg.content)
    if match:
        p={
            "s":match,
            "limit":"3",
            "type":"1",
            "offset":"0"
        }
        h={"Referer":"http://music.163.com"}
        c={"appver":"2.0.2"}
        r=requests.post(url,data=p,headers=h,cookies=c)
        r_list=r.json().get("result").get("songs")
        s=""
        for i in r_list:
            s+=i.get("name")+"：http://music.163.com/#/song?id="+i.get("id")+"\n"
        bot.reply_msg(msg, s)
        return True
    return False