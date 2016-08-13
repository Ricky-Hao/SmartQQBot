# coding:utf-8
import requests
import json
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
# Code by:      john123951  /   john123951@126.com
# Modify by:    Yinzo       /   yinz995-1@yahoo.com

######
KEY = '31662bc776555612e3639dbca1ad1fd5'
plugin_name='Weather'
HELP={
    1,'Weather: 天气查询插件',
    2,'天气 城市: 查询某城市天气，暂只支持国内城市'
}
######

######

######

######

######



@on_all_message(name=plugin_name)
def weather(msg, bot):
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugin_name) and utils.is_match(r'^天气 (.*)$',msg.content):
        city=utils.is_match(r'^天气 (.*)$',msg.content).group(1)
        logger.info("[Weather] "+account_type+': '+account+" "+city)

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
