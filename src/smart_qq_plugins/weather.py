# coding:utf-8
import requests
import json
import re
import sqlite3
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message

# Code by:      john123951  /   john123951@126.com
# Modify by:    Yinzo       /   yinz995-1@yahoo.com

KEY = '31662bc776555612e3639dbca1ad1fd5'

con = sqlite3.connect("./config/data.db")
cur=con.cursor()
cur.execute('select uin from uin_plugins where plugin_name="weather";')
a=cur.fetchall()
uin=[]
for i in a:
    uin.append(i[0])
cur.close()
con.close()

@on_all_message(name='weather')
def weather(msg, bot):
    global query
    if str(msg.from_uin) in uin:
        match = re.match(r'^(weather|天气) (\w+|[\u4e00-\u9fa5]+)', msg.content)
        if match:
            logger.info("RUNTIMELOG 查询天气...")
            command = match.group(1)
            city = match.group(2)
            logger.info("RUNTIMELOG 查询天气语句: " + msg.content)
            if command == 'weather' or command == '天气':
                try:
                    city_name = city
                    url_str = "http://api.map.baidu.com/telematics/v3/weather?location={city}&ak={key}&output=json".format(
                        city=city_name,
                        key=KEY
                    )
                    response = requests.get(url_str)
                    data_html = response.text
                    logger.debug("RESPONSE " + data_html)
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
                return True
    return False
