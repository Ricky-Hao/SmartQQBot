#coding=utf-8
import requests
import re

from smart_qq_bot.logger import logger
from smart_qq_bot.messages import GroupMsg
from smart_qq_bot.signals import on_all_message, on_bot_inited

@on_all_message(name="NetEaseMusic")
def NetEaseMusic(msg,bot):
    match = re.match('^(music|音乐) (\w+|[\u4e00-\u9fa5]+)', msg.content)
    if match:
        url="http://music.163.com/api/search/get/"
        p={
            "s":msg.content[3:],
            "limit":"3",
            "type":"1",
            "offset":"0"
        }
        h={"Referer":"http://music.163.com"}
        c={"appver":"2.0.2"}
        r=requests.post(url,data=p,headers=h,cookies=c)
        r_list=r.json().get("result").get("songs")
        s=""
        if isinstance(r_list,list): 
            for i in r_list:
                s+="歌曲名："+i.get("name")+"   歌手："+i.get("artists")[0].get("name")+"\nhttp://music.163.com/#/song?id="+str(i.get("id"))+"\n"
            bot.reply_msg(msg, s)
        else:
            bot.reply_msg(msg,"没有找到音乐哦")
        return True
    return False
