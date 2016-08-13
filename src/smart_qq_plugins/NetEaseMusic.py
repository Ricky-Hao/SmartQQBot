#coding=utf-8
import requests
from smart_qq_bot.logger import logger
import smart_qq_bot.sqlite as sql
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.utils as utils

######
plugin_name="NetEaseMusic"
HELP={
    1:'NetEaseMusic: 网易云音乐在线查询插件',
    2:'音乐 乐曲名: 自动搜索该乐曲名音乐，并显示前三条'
}
######

######

######

######

######

######
@on_all_message(name="NetEaseMusic")
def NetEaseMusic(msg,bot):
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugin_name) and utils.is_match(r'^音乐 (.*)$',msg.content):
        music_name=utils.is_match(r'^音乐 (.*)$',msg.content).group(1)
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
