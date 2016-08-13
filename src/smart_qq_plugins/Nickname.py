# -*- coding: utf-8 -*-
import random
import re
import json
import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message

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
HELP={
    'Nickname':'昵称插件',
    '!昵称 rename 新昵称':'为机器人改名',
    '!昵称 list content':'列出机器人自动回复的内容列表',
    '!昵称 list suffix':'列出机器人自动回复的后缀列表',
    '!昵称 add content xxx':'将xxx添加入机器人自动回复的内容列表',
    '!昵称 add suffix xxx':'将xxx添加入机器人自动回复的后缀列表',
    '!昵称 remove content xxx':'将xxx从机器人自动回复的内容列表中移除',
    '!昵称 remove suffix xxx':'将xxx从机器人自动回复的后缀列表中移除'
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
