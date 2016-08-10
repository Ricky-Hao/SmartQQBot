#coding=utf-8
import requests
import re
import sqlite3
from smart_qq_bot.logger import logger
import smart_qq_bot.sqlite as sql
from smart_qq_bot.signals import on_all_message

######
plugin_name="NetEaseMusic"
######

######
def update_id(name):
    global group_id
    global private_id
    
    private_id=sql.get_private_id(name)
    group_id=sql.get_group_id(name)

def in_group(gc):
    global group_id
    return gc in group_id

def in_private(qq):
    global private_id
    return qq in private_id

def is_match(p,s):
    return re.match(p,s)
######

######
update_id(plugin_name)
######

######
@on_all_message(name="NetEaseMusic")
def NetEaseMusic(msg,bot):
    update_id(plugin_name)
    if msg.type=="group_message":
        number=msg.group_id
    else:
        number=msg.private_id
    if (in_group(number) or in_private(number)) and is_match(r'^音乐 (.*)$',msg.content):
        music_name=is_match(r'^音乐 (.*)$',msg.content).group(1)
        url="http://music.163.com/api/search/get/"
        p={
            "s":music_name,
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
