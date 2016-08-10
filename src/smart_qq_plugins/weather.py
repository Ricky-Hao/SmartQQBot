# coding:utf-8
import requests
import json
import re
import sqlite3
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql

# Code by:      john123951  /   john123951@126.com
# Modify by:    Yinzo       /   yinz995-1@yahoo.com

######
KEY = '31662bc776555612e3639dbca1ad1fd5'
plugin_name='Weather'
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



@on_all_message(name=plugin_name)
def weather(msg, bot):
    update_id(plugin_name)
    if msg.type=="group_message":
        number=bot.msg_to_group_id(msg)
    else:
        number=str(bot.uin_to_account(msg.from_uin))
    if (in_group(number) or in_private(number)) and is_match(r'^天气 (.*)$',msg.content):
        city=is_match(r'^天气 (.*)$',msg.content).group(1)
        logger.info("[Weather] "+number+" "+city)

        try:
            city_name = city
            url_str = "http://api.map.baidu.com/telematics/v3/weather?location={city}&ak={key}&output=json".format(
                city=city_name,
                key=KEY
            )
            response = requests.get(url_str)
            data_html = response.text
            json_result = json.loads(data_html)['results'][0]

            str_data = ""
            str_data += json_result['currentCity'] + " PM:" + json_result['pm25'] + "\n"
            try:
                str_data += json_result["index"][0]['des'] + "\n"
            except:
                pass

            for data in json_result["weather_data"]:
                str_data += data['date'] + " "
                str_data += data['weather'] + " "
                str_data += data['wind'] + " "
                str_data += data['temperature']
                str_data += '\n'
        except:
            str_data = "Not found city"

        bot.reply_msg(msg, str_data)
