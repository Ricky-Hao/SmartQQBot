# -*- coding: utf-8 -*-
import random
import re
import json
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message

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
HELP={
    1:'Nickname: 昵称插件',
    2:'!昵称 rename 新昵称: 为机器人改名',
    3:'!昵称 list content: 列出机器人自动回复的内容列表',
    4:'!昵称 list suffix: 列出机器人自动回复的后缀列表',
    5:'!昵称 add content xxx: 将xxx添加入机器人自动回复的内容列表',
    6:'!昵称 add suffix xxx: 将xxx添加入机器人自动回复的后缀列表',
    7:'!昵称 remove content xxx: 将xxx从机器人自动回复的内容列表中移除',
    8:'!昵称 remove suffix xxx: 将xxx从机器人自动回复的后缀列表中移除'
}

#########内部函数#################
def Nickname_init():
    '''
    Nickname 数据库初始化函数
    '''
    sql.execute("create table if not exists Nickname(id integer primary key autoincrement unique not null, \
    nickname varchar(100), account varchar(40), content varchar(1000), suffix varchar(100),account_type varchar(20));")
    sql.execute("insert into Nickname(account,nickname,content,suffix,account_type) values('{0}','{1}','{2}','{3}','{4}');".format("00000","baseline",json.dumps(REPLY_CONTENT),json.dumps(REPLY_SUFFIX),'group'))
    
#########初始化代码#################
#判断插件是否已经初始化（即存不存在插件名的数据库）
if not utils.check_table(plugin_name):
    Nickname_init()
#########调用函数##################

#################################################################
#注册该函数到 on_all_message handler
#唤出函数
@on_all_message(name=plugin_name)
def Nickname(msg, bot):
    (account,account_type)=utils.get_account_and_type(msg)
    #检查该群是否启用该插件
    if utils.in_plugins(account,account_type,plugin_name):
        '''
        使用正则判断
        例：
            nickname~  True
            nickname~~ False
        '''
        nickname=sql.fetch_one('select nickname from Nickname where account="{0}" and account_type="{1}";'.format(account,account_type))[0]
        if utils.is_match('^'+nickname+r'.{0,1}$',msg.content):
            #在控制台输出log信息
            logger.info("[Nickname] " + account_type+': '+account + " calling me out, trying to reply....")

            #从 该插件表 中获取一条制定群号的 content,suffix 数据
            tmp=sql.fetch_one('select content,suffix from Nickname where account="{0}" and account_type="{1}"'.format(account,account_type))
            '''
            从数据库加载content和suffix并用json解析，随机选择一个
            '''
            bot.reply_msg(msg,random.choice(json.loads(tmp[0]))+random.choice(json.loads(tmp[1])))

            #列表功能
        elif utils.is_match('^!'+nickname+' list (content|suffix)$',msg.content):
            #提取操作数content或者suffix
            opt=utils.is_match('^!'+nickname+' list (content|suffix)$',msg.content).group(1)
            #在控制台输出log信息
            logger.info("[Nickname] "+account_type+": "+account+" list "+opt)
            s=""
            #读取数据库相应数据，解析成json并拼接为回复内容
            tmp=json.loads(sql.fetch_one('select {0} from Nickname where account="{1}" and account_type="{2}";'.format(opt,account,account_type))[0])
            for i in tmp:
                s+=i+'\n'
            bot.reply_msg(msg,s)

            #添加功能
        elif utils.is_match('^!'+nickname+' add (content|suffix) (.*)$',msg.content):
            #从命令中捕获操作数及数据
            opt=utils.is_match('^!'+nickname+' add (content|suffix) (.*)$',msg.content).group(1)
            content=utils.is_match('^!'+nickname+' add (content|suffix) (.*)$',msg.content).group(2)
            #写入数据库
            #先将数据库内的数据解析成list
            tmp=json.loads(sql.fetch_one('select {0} from Nickname where account="{1}" and account_type="{2}";'.format(opt,account,account_type))[0])
            #将content加入list
            tmp.append(content)
            #将list转换为json写入数据库
            sql.execute("update Nickname set '{0}' = '{1}' where account = '{2}' and account_type='{3}';".format(opt,json.dumps(tmp),account,account_type))

        elif utils.is_match('^!'+nickname+' remove (content|suffix) (.*)$',msg.content):
            #从命令中捕获操作数及数据
            opt=utils.is_match('^!'+nickname+' remove (content|suffix) (.*)$',msg.content).group(1)
            content=utils.is_match('^!'+nickname+' remove (content|suffix) (.*)$',msg.content).group(2)
            #写入数据库
            #先将数据库内的数据解析成list
            tmp=json.loads(sql.fetch_one('select {0} from Nickname where account="{1}" and account_type="{2}";'.format(opt,account,account_type))[0])
            if content in tmp:
                tmp.remove(content)
                #将list转换为json写入数据库
                sql.execute("update Nickname set '{0}' = '{1}' where account = '{2}' and account_type='{3}';".format(opt,json.dumps(tmp),account,account_type))
            else:
                bot.reply_msg(msg,'没有这个内容哦！')

        elif utils.is_match('^!'+nickname+' rename (.*)$',msg.content):
            rename=utils.is_match('^!'+nickname+' rename (.*)$',msg.content).group(1)
            logger.info('[Nickname] '+account_type+": "+account+' rename to '+rename)
            sql.execute('update Nickname set nickname = "{0}" where account = "{1}" and account_type="{2}";'.format(rename,account,account_type))
            bot.reply_msg(msg,'大召唤术！'+rename)
