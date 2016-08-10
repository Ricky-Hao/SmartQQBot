# -*- coding: utf-8 -*-
import random
import re
import json
import sqlite3
import smart_qq_bot.sqlite as sql
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
)

######################插件编写教程#########################
#sql库是内置的对数据库进行操作的一个接口
#其提供了
#   sql.execute(s)      ：用于执行不需要返回值的sql命令。s：字符串
#   sql.fetch_all(s)    ：用于执行需要返回全部结果的sql命令。s：字符串
#   sql.fetch_one(s)    ：用于执行需要返回一条结果的sql命令。s：字符串
#   sql.get_private_id(plugin_name)    ：从 plugins_private表 中提取启用了 plugin_name 插件的 QQ号 数据，
#                                       并以列表的形式储存在private_id。返回值：private_id=['xxx','sss']
#   sql.get_group_id(plugin_name)    ：从 plugins_group表 中提取启用了 plugin_name 插件的 群号 数据，
#                                       并以列表的形式储存在group_id。返回值：group_id=['xxx','sss']
#   sql.check_table(table_name)     ：用于检测表 table_name 是否已存在（即插件是否已数据库初始化）。
#                                   返回值： True 已初始化，False 未初始化
#==========================================================
#logger是向控制台输出消息的对象
#   logger.info(string)     输出Info信息
#   logger.debug(string)    输出Debug信息，仅在Debug模式有效
#   logger.error(string)    输出错误信息
#==========================================================
#signals分为三种
#   on_all_message      所有信息都将被送往标记函数
#   on_group_message    只有群消息将被送往标记函数
#   on_private_message  只有私聊消息将被送往标记函数
#如何标记函数
#@on_all_message(name='plugin_name')
#def marked_fun(msg,bot)
#   其中msg为需要处理的消息，bot为机器人对象
#==========================================================
#msg的属性
#   msg.content     消息的文本内容
#   msg.from_uin    消息的发送uin，为int类型
#
#bot的方法
#   bot.get_group_info(group_code=str(msg.from_uin))    获取群消息msg发送者的群信息
#                                                       返回字典类型
#                                                       {
#                                                           'name':         "群名",
#                                                           'id':            12345678,
#                                                           'group_code':    87654321
#                                                       }
#   bot.uin_to_account(msg.from_uin))                   返回私聊消息msg发送者的QQ号
#                                                       返回int型
#===========================================================
#插件大体可以分为四部分
#一、常量部分
#   定义下文需要用到的各种常量
#二、初始化代码部分
#   该部分代码用于判断及初始化插件数据库。
#   初始化插件的加载。
#   刷新数据等等。
#三、内部函数部分
#   定义需要用到的内部函数
#四、调用函数部分
#   该部分函数将会被 signals 标记，即会有消息被送往
############################################################


# =====唤出插件=====

# 机器人连续回复相同消息时可能会出现
# 服务器响应成功,但实际并没有发送成功的现象
# 所以尝试通过随机后缀来尽量避免这一问题
plugin_name='Nickname'
REPLY_SUFFIX = [
    '~',
    '!',
    '?',
    '||',
]
REPLY_CONTENT=[
    "干嘛（‘·д·）",
    "嗯",
    "肿么了",
    "在呀",
    "不约",
    "嗯哼",
    "啊哈"
]

#########内部函数#################
def Nickname_init():
    '''
    Nickname 数据库初始化函数
    '''
    sql.execute("create table if not exists Nickname_group(id integer primary key autoincrement unique not null, \
    nickname varchar(100), group_id varchar(40), content varchar(1000), suffix varchar(100));")
    sql.execute("insert into Nickname_group(group_id,nickname,content,suffix) values('{0}','{1}','{2}','{3}')".format("00000","baseline",json.dumps(REPLY_CONTENT),json.dumps(REPLY_SUFFIX)))
    
    sql.execute("create table if not exists Nickname_private(id integer primary key autoincrement unique not null, \
    nickname varchar(100), private_id varchar(40), content varchar(1000), suffix varchar(100));")
    sql.execute("insert into Nickname_private(private_id,nickname,content,suffix) values('{0}','{1}','{2}','{3}')".format("00000","baseline",json.dumps(REPLY_CONTENT),json.dumps(REPLY_SUFFIX)))

def is_match(p,s):
    return re.match(p,s)

def get_group_data():
    #从 Nickname_group 中提取 群号：昵称 数据，并以字典的形式储存group_data{'group_id':'nickname'}
    tmp=sql.fetch_all('select group_id,nickname from Nickname_group;')
    group_data={}
    for i in tmp:
        group_data[i[0]]=i[1]
    return group_data

def get_private_data():
    #从 Nickname_group 中提取 QQ号：昵称 数据，并以字典的形式储存private_data{'private_id':'nickname'}
    tmp=sql.fetch_all('select private_id,nickname from Nickname_private;')
    private_data={}
    for i in tmp:
        private_data[i[0]]=i[1]
    return private_data

def update_data(name):
    global group_id
    global group_data
    global private_id
    global private_data
    
    private_id=sql.get_private_id(name)
    private_data=get_private_data()
    group_id=sql.get_group_id(name)
    group_data=get_group_data()

def in_group(gc):
    global group_id
    return gc in group_id

def in_private(qq):
    global private_id
    return qq in private_id

#########初始化代码#################
#判断插件是否已经初始化（即存不存在插件名的数据库）
if not sql.check_table(plugin_name+'_group'):
    Nickname_init()
#更新数据
update_data(plugin_name)

#########调用函数##################

##########################群版本#######################################
#注册该函数到 on_group_message handler
#唤出函数
@on_group_message(name=plugin_name)
def group_callout(msg, bot):
    '''
    从消息msg中，提取from_uin
    从bot对象中，用msg.from_uin来通过bot.get_group_info()函数提取对应的群信息
    {
        'name':         "群名",
        'id':            12345678,
        'group_code':    87654321
    }
    '''
    update_data(plugin_name)
    global group_data

    gc=msg.group_id
    #检查该群是否启用该插件
    if in_group(gc):
        '''
        使用正则判断
        例：
            nickname~  True
            nickname~~ False
        '''
        if is_match('^'+group_data[gc]+r'.{0,1}$',msg.content):
            #在控制台输出log信息
            logger.info("[Nickname] " + gc + " calling me out, trying to reply....")

            #从 该插件表 中获取一条制定群号的 content,suffix 数据
            tmp=sql.fetch_one('select content,suffix from Nickname_group where group_id="{0}"'.format(gc))
            '''
            从数据库加载content和suffix并用json解析，随机选择一个
            '''
            bot.reply_msg(msg,random.choice(json.loads(tmp[0]))+random.choice(json.loads(tmp[1])))

#控制函数
#可以列出、增、删content,suffix
@on_group_message(name=plugin_name)
def group_control(msg,bot):
    update_data(plugin_name)
    gc=msg.group_id
    #检查该群是否启用该插件
    if in_group(gc):
        name=group_data[gc]
        #logger.debug(name)
        if is_match('^!'+name+' list (content|suffix)$',msg.content):
            #提取操作数content或者suffix
            opt=is_match('^!'+name+' list (content|suffix)$',msg.content).group(1)
            #在控制台输出log信息
            logger.info("[Nickname] "+gc+" list "+opt)
            s=""
            #读取数据库相应数据，解析成json并拼接为回复内容
            tmp=json.loads(sql.fetch_one('select {0} from Nickname_group where group_id="{1}";'.format(opt,gc))[0])
            for i in tmp:
                s+=i+'\n'
            bot.reply_msg(msg,s)
            update_data(plugin_name)

        elif is_match('^!'+name+' add (content|suffix) (.*)$',msg.content):
            #从命令中捕获操作数及数据
            opt=is_match('^!'+name+' add (content|suffix) (.*)$',msg.content).group(1)
            content=is_match('^!'+name+' add (content|suffix) (.*)$',msg.content).group(2)
            #写入数据库
            #先将数据库内的数据解析成list
            tmp=json.loads(sql.fetch_one('select {0} from Nickname_group where group_id="{1}";'.format(opt,gc))[0])
            #将content加入list
            tmp.append(content)
            #将list转换为json写入数据库
            sql.execute("update Nickname_group set '{0}' = '{1}' where group_id = '{2}';".format(opt,json.dumps(tmp),gc))
            update_data(plugin_name)

        elif is_match('^!'+name+' remove (content|suffix) (.*)$',msg.content):
            #从命令中捕获操作数及数据
            opt=is_match('^!'+name+' remove (content|suffix) (.*)$',msg.content).group(1)
            content=is_match('^!'+name+' remove (content|suffix) (.*)$',msg.content).group(2)
            #写入数据库
            #先将数据库内的数据解析成list
            tmp=json.loads(sql.fetch_one('select {0} from Nickname_group where group_id="{1}";'.format(opt,gc))[0])
            #将content加入list
            tmp.remove(content)
            #将list转换为json写入数据库
            sql.execute("update Nickname_group set '{0}' = '{1}' where group_id = '{2}';".format(opt,json.dumps(tmp),gc))
            update_data(plugin_name)
        elif is_match('^!'+name+' rename (.*)$',msg.content):
            rename=is_match('^!'+name+' rename (.*)$',msg.content).group(1)
            logger.info('[Nickname] '+gc+' rename to '+rename)
            sql.execute('update Nickname_group set nickname = "{0}" where group_id = "{1}";'.format(rename,gc))
            bot.reply_msg(msg,'大召唤术！'+rename)
            update_data(plugin_name)

##################私聊版本#####################################
#注册该函数到 on_private_message handler
#唤出函数
@on_private_message(name=plugin_name)
def private_callout(msg,bot):
    '''
    从消息msg中，提取from_uin
    从bot对象中，用msg.from_uin来通过bot.uin_to_account()函数提取对应的QQ号
    '''
    update_data(plugin_name)
    global private_data
    qq=msg.private_id
    #检查该群是否启用该插件
    if in_private(qq):
        '''
        使用正则判断
        例：
            nickname~  True
            nickname~~ False
        '''
        if is_match('^'+private_data[qq]+r'.{0,1}$',msg.content):
            #在控制台输出log信息
            logger.info("[Nickname] " + qq + " calling me out, trying to reply....")

            #从 该插件表 中获取一条制定群号的 content,suffix 数据
            tmp=sql.fetch_one('select content,suffix from Nickname_private where private_id="{0}"'.format(qq))
            '''
            从数据库加载content和suffix并用json解析，随机选择一个
            '''
            bot.reply_msg(msg,random.choice(json.loads(tmp[0]))+random.choice(json.loads(tmp[1])))

#控制函数
#可以列出、增、删content,suffix
@on_private_message(name=plugin_name)
def private_control(msg,bot):
    update_data(plugin_name)
    qq=msg.private_id
    #检查该群是否启用该插件
    if in_private(qq):
        name=private_data[qq]
        if is_match('^!'+name+' list (content|suffix)$',msg.content):
            #提取操作数content或者suffix
            opt=is_match('^!'+name+' list (content|suffix)$',msg.content).group(1)
            #在控制台输出log信息
            logger.info("[Nickname] "+qq+" list "+opt)
            s=""
            #读取数据库相应数据，解析成json并拼接为回复内容
            tmp=json.loads(sql.fetch_one('select {0} from Nickname_private where private_id="{1}";'.format(opt,qq))[0])
            for i in tmp:
                s+=i+'\n'
            bot.reply_msg(msg,s)
            update_data(plugin_name)

        elif is_match('^!'+name+' add (content|suffix) (.*)$',msg.content):
            #从命令中捕获操作数及数据
            opt=is_match('^!'+name+' add (content|suffix) (.*)$',msg.content).group(1)
            content=is_match('^!'+name+' add (content|suffix) (.*)$',msg.content).group(2)
            #写入数据库
            #先将数据库内的数据解析成list
            tmp=json.loads(sql.fetch_one('select {0} from Nickname_private where private_id="{1}";'.format(opt,qq))[0])
            #将content加入list
            tmp.append(content)
            #将list转换为json写入数据库
            sql.execute("update Nickname_private set '{0}' = '{1}' where private_id = '{2}';".format(opt,json.dumps(tmp),qq))
            update_data(plugin_name)

        elif is_match('^!'+name+' remove (content|suffix) (.*)$',msg.content):
            #从命令中捕获操作数及数据
            opt=is_match('^!'+name+' remove (content|suffix) (.*)$',msg.content).group(1)
            content=is_match('^!'+name+' remove (content|suffix) (.*)$',msg.content).group(2)
            #写入数据库
            #先将数据库内的数据解析成list
            tmp=json.loads(sql.fetch_one('select {0} from Nickname_private where private_id="{1}";'.format(opt,qq))[0])
            #将content加入list
            tmp.remove(content)
            #将list转换为json写入数据库
            sql.execute("update Nickname_private set '{0}' = '{1}' where private_id = '{2}';".format(opt,json.dumps(tmp),qq))
            update_data(plugin_name)
        elif is_match('^!'+name+' rename (.*)$',msg.content):
            rename=is_match('^!'+name+' rename (.*)$',msg.content).group(1)
            logger.info('[Nickname] '+qq+' rename to '+rename)
            sql.execute('update Nickname_private set nickname = "{0}" where private_id = "{1}";'.format(rename,qq))
            bot.reply_msg(msg,'大召唤术！'+rename)
            update_data(plugin_name)