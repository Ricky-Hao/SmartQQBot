import sqlite3
import re
import smart_qq_bot.sqlite as sql
from smart_qq_plugins.Nickname import REPLY_CONTENT,REPLY_SUFFIX
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_private_message, on_group_message
import json

########################
plugin_name="Activate"

########################

#######################
def is_match(p,s):
    return re.match(p,s)

def update_data(name):
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
#######################

#######################
update_data(plugin_name)
#######################

#######################
@on_group_message(name=plugin_name)
def do_Activate(msg,bot):
    #获取群号
    gc=msg.group_id
    if not in_group(gc) and is_match(r'^!召唤 (.*)$',msg.content):
        #捕获昵称
        nickname=is_match(r'^!召唤 (.*)$',msg.content).group(1)
        #将昵称和群号绑定
        sql.execute("insert into Nickname_group(group_id,nickname,content,suffix) values('{0}','{1}','{2}','{3}');".format(gc,nickname,json.dumps(REPLY_CONTENT),json.dumps(REPLY_SUFFIX)))
        #默认激活所有插件
        with open('./config/plugin.json','r') as f:
            plugin_list=json.load(f).get('plugin_on')
        for p in plugin_list:
            sql.execute("insert into plugins_group(group_id,plugin_name) values('{0}','{1}');".format(gc,p))
        logger.info('[Activate] '+gc+' activate success')
        bot.reply_msg(msg,'召唤'+nickname+'成功~')
        update_data(plugin_name)

    elif in_group(gc) and is_match(r'^!召唤 (.*)$',msg.content):
        #捕获昵称
        nickname=is_match(r'^!召唤 (.*)$',msg.content).group(1)
        bot.reply_msg(msg,'已经召唤过'+nickname+'啦~')

    #关闭插件
    elif in_group(gc) and is_match(r'^!关闭 (.*)$',msg.content):
        #获取插件名称
        close_plugin_name=is_match(r'^!关闭 (.*)$',msg.content).group(1)
        if close_plugin_name != 'Activate':
            #从数据库中删除群号-插件关系
            sql.execute("delete from plugins_group where group_id={0} and plugin_name='{1}';".format(gc,close_plugin_name))
            logger.info('[Activate] '+gc+' inactivate '+close_plugin_name)
            bot.reply_msg(msg,"关闭{0}插件成功~".format(close_plugin_name))
            update_data(plugin_name)
        else:
            bot.reply_msg(msg,'不能关闭Activate插件哦~')

    #启用插件
    elif in_group(gc) and is_match(r'^!启用 (.*)$',msg.content):
        open_plugin_name=is_match(r'^!启用 (.*)$',msg.content).group(1)
        sql.execute("insert into plugins_group(group_id,plugin_name) values ('{0}','{1}');".format(gc,open_plugin_name))
        logger.info('[Activate] '+gc+' activate '+open_plugin_name)
        bot.reply_msg(msg,"开启{0}插件成功~".format(open_plugin_name))
        update_data(plugin_name)

    #列出插件列表
    elif in_group(gc) and is_match(r'^!已启用插件$',msg.content):
        l=sql.fetch_all('select plugin_name from plugins_group where group_id="{0}";'.format(gc))
        s="已启用插件：\n"
        for i in l:
            s+=i[0]+'\n'
        bot.reply_msg(msg,s)


@on_private_message(name=plugin_name)
def do_Activate(msg,bot):
    #获取群号
    qq=msg.private_id
    if not in_private(qq) and is_match(r'^!召唤 (.*)$',msg.content):
        #捕获昵称
        nickname=is_match(r'^!召唤 (.*)$',msg.content).group(1)
        #将昵称和群号绑定
        sql.execute("insert into Nickname_private(private_id,nickname,content,suffix) values('{0}','{1}','{2}','{3}');".format(qq,nickname,json.dumps(REPLY_CONTENT),json.dumps(REPLY_SUFFIX)))
        #默认激活所有插件
        with open('./config/plugin.json','r') as f:
            plugin_list=json.load(f).get('plugin_on')
        for p in plugin_list:
            sql.execute("insert into plugins_private(private_id,plugin_name) values('{0}','{1}');".format(qq,p))
        logger.info('[Activate] '+qq+' activate success')
        bot.reply_msg(msg,'召唤'+nickname+'成功~')
        update_data(plugin_name)
    elif in_private(qq) and is_match(r'^!召唤 (.*)$',msg.content):
        #捕获昵称
        nickname=is_match(r'^!召唤 (.*)$',msg.content).group(1)
        bot.reply_msg(msg,'已经召唤过'+nickname+'啦~')

    #关闭插件
    elif in_private(qq) and is_match(r'^!关闭 (.*)$',msg.content):
        #获取插件名称
        close_plugin_name=is_match(r'^!关闭 (.*)$',msg.content).group(1)
        if close_plugin_name != 'Activate':
            #从数据库中删除群号-插件关系
            sql.execute("delete from plugins_private where private_id={0} and plugin_name='{1}';".format(qq,close_plugin_name))
            logger.info('[Activate] '+qq+' inactivate '+close_plugin_name)
            bot.reply_msg(msg,"关闭{0}插件成功~".format(close_plugin_name))
            update_data(plugin_name)
        else:
            bot.reply_msg(msg,'不能关闭Activate插件哦~')

    #启用插件
    elif in_private(qq) and is_match(r'^!启用 (.*)$',msg.content):
        open_plugin_name=is_match(r'^!启用 (.*)$',msg.content).group(1)
        sql.execute("insert into plugins_private(private_id,plugin_name) values ('{0}','{1}');".format(qq,open_plugin_name))
        logger.info('[Activate] '+qq+' activate '+open_plugin_name)
        bot.reply_msg(msg,"开启{0}插件成功~".format(open_plugin_name))
        update_data(plugin_name)

    #列出插件列表
    elif in_private(qq) and is_match(r'^!已启用插件$',msg.content):
        l=sql.fetch_all('select plugin_name from plugins_private where private_id="{0}";'.format(qq))
        s="已启用插件：\n"
        for i in l:
            s+=i[0]+'\n'
        bot.reply_msg(msg,s)
