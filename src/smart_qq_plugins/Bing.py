# coding:utf-8
import requests
import json
import re
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import smart_qq_bot.sqlite as sql

######
with open('./config/API_Key.json','r') as f:
    API_KEY=json.load(f)
plugin_name='Bing'
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
@on_all_message(name=plugin_name)
def Bing(msg,bot):
    update_id(plugin_name)
    if msg.type=="group_message":
        number=msg.group_id
    else:
        number=msg.private_id
    if (in_group(number) or in_private(number)) and is_match('^搜索 (.*)$',msg.content):
        headers={'Ocp-Apim-Subscription-Key':API_KEY.get('Bing')}
        params={
            'q':is_match('^搜索 (.*)$',msg.content).group(1),
            'count':'3'
            }
        tmp=json.loads(requests.get('https://api.cognitive.microsoft.com/bing/v5.0/search',headers=headers,params=params).text).get("webPages").get("value")
        s=""
        for i in tmp:
            s+=i['name']+'\n'+i['url']+'\n'
        bot.reply_msg(msg,s)
    elif (in_group(number) or in_private(number)) and is_match('^翻译 (日|英|)\s?(.*)$',msg.content):
        key_word=is_match('^翻译 (日|英|)\s?(.*)$',msg.content).group(2)
        opt=is_match('^翻译 (日|英|)\s?(.*)$',msg.content).group(1)
        data={
            'client_id':'Smart_QQ_Bot',
            'client_secret':API_KEY.get('Azure_Smart_QQ_Bot'),
            'scope':'http://api.microsofttranslator.com/',
            'grant_type':'client_credentials'
        }
        access_token=json.loads(requests.post('https://datamarket.accesscontrol.windows.net/v2/OAuth2-13',data=data).text).get('access_token')
        headers={'Authorization':'bearer '+access_token}
        from_lang=requests.get('http://api.microsofttranslator.com/V2/Http.svc/Detect',headers=headers,params={'text':key_word})
        from_lang=is_match('^<.*>(.*)</string>$',from_lang.text).group(1)

        if opt=='日':
            to_lang='ja'
        elif opt=='英':
            to_lang='en'
        else:
            to_lang='zh-CHS'

        params={
            'text':key_word,
            'to':to_lang,
            'from':from_lang
        }
        tmp=requests.get('http://api.microsofttranslator.com/V2/Http.svc/Translate',headers=headers,params=params)
        bot.reply_msg(msg,is_match('^<.*>(.*)</string>$',tmp.text).group(1))
