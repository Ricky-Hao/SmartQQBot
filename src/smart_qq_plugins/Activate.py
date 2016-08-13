import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
from smart_qq_plugins.Nickname import REPLY_CONTENT,REPLY_SUFFIX
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import json

########################
plugin_name="Activate"
HELP={
    1:'Activate: 控制插件',
    2:'!召唤 昵称: 将机器人命名为“昵称”，并启用',
    3:'!回去吧 昵称: 将机器人关闭（需要事先起用）',
    4:'!已启用插件: 获得已启用插件列表',
    5:'!可用插件: 获得可用插件列表',
    6:'!启用 插件名称: 开启插件',
    7:'!关闭 插件名称: 关闭插件'
}
########################

#######################

#######################

#######################

#######################

#######################
@on_all_message(name=plugin_name)
def do_Activate(msg,bot):
    #获取群号
    (account,account_type)=utils.get_account_and_type(msg)
    if not utils.in_plugins(account,account_type,plugin_name) and utils.is_match(r'^!召唤 (.*)$',msg.content):
        #捕获昵称
        nickname=utils.is_match(r'^!召唤 (.*)$',msg.content).group(1)
        #将昵称和账号绑定
        sql.execute("insert into Nickname(account,nickname,content,suffix,account_type) values('{0}','{1}','{2}','{3}','{4}');".format(account,nickname,json.dumps(REPLY_CONTENT),json.dumps(REPLY_SUFFIX),account_type))
        #默认激活所有插件
        with open('./config/plugin.json','r') as f:
            plugin_list=json.load(f).get('plugin_on')
        for p in plugin_list:
            sql.execute("insert into plugins(account,plugin_name,account_type) values('{0}','{1}','{2}');".format(account,p,account_type))
        logger.info('[Activate] '+account_type+': '+account+' activate success')
        bot.reply_msg(msg,'召唤'+nickname+'成功~')

    elif utils.in_plugins(account,account_type,plugin_name):
        if utils.is_match(r'^!召唤 (.*)$',msg.content):
            #捕获昵称
            nickname=utils.is_match(r'^!召唤 (.*)$',msg.content).group(1)
            bot.reply_msg(msg,'已经召唤过'+nickname+'啦~')

        #关闭插件
        elif utils.is_match(r'^!关闭 (.*)$',msg.content):
            #获取插件名称
            close_plugin_name=utils.is_match(r'^!关闭 (.*)$',msg.content).group(1)
            if close_plugin_name != 'Activate':
                #从数据库中删除群号-插件关系
                l=sql.fetch_all('select plugin_name from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
                tmp=[]
                for i in l:
                    tmp.append(i[0])
                if close_plugin_name in tmp:
                    sql.execute("delete from plugins where account={0} and plugin_name='{1}' and account_type='{2}';".format(account,close_plugin_name,account_type))
                    logger.info('[Activate] '+account_type+': '+account+' inactivate '+close_plugin_name)
                    bot.reply_msg(msg,"关闭{0}插件成功~".format(close_plugin_name))
                else:
                    bot.reply_msg(msg,close_plugin_name+'插件还没开启呢！')
            else:
                bot.reply_msg(msg,'不能关闭Activate插件哦~')

        #启用插件
        elif utils.is_match(r'^!启用 (.*)$',msg.content):
            open_plugin_name=utils.is_match(r'^!启用 (.*)$',msg.content).group(1)
            tmp=sql.fetch_all('select plugin_name from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
            open_list=[]
            for i in open_list:
                open_list.append(i[0])

            with open('./config/plugin.json','r') as f:
                plugin_list=json.load(f).get('plugin_on')

            if open_plugin_name not in open_list and open_plugin_name in plugin_list:
                sql.execute("insert into plugins(account,plugin_name,account_type) values ('{0}','{1}','{2}');".format(account,open_plugin_name,account_type))
                logger.info('[Activate] '+account_type+': '+account+' activate '+open_plugin_name)
                bot.reply_msg(msg,"开启{0}插件成功~".format(open_plugin_name))
            elif open_plugin_name in open_list:
                bot.reply_msg(msg,open_plugin_name+'已经在使用了哦~')
            else:
                bot.reply_msg(msg,'别捣乱，哼哼~')

        #列出插件列表
        elif utils.is_match(r'^!已启用插件$',msg.content):
            l=sql.fetch_all('select plugin_name from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
            s="已启用插件：\n"
            for i in l:
                s+=i[0]+'\n'
            bot.reply_msg(msg,s)

        #列出可用插件
        elif utils.is_match(r'^!可用插件$',msg.content):
            s=""
            with open('./config/plugin.json','r') as f:
                plugin_list=json.load(f).get('plugin_on')
            tmp=sql.fetch_all('select plugin_name from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
            l=[]
            for i in tmp:
                l.append(i[0])
            for p in plugin_list:
                if p not in l:
                    s+=p+'\n'
            if s!="":
                bot.reply_msg(msg,s)
            else:
                bot.reply_msg(msg,'全部插件都启用了啦~')

        #完全关闭
        elif utils.is_match(r'^!回去吧 (.*)$',msg.content):
            m_nickname=utils.is_match(r'^!回去吧 (.*)$',msg.content).group(1)
            nickname=sql.fetch_one('select nickname from Nickname where account="{0}" and account_type="{1}";'.format(account,account_type))[0]
            if m_nickname==nickname:
                sql.execute('delete from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
                bot.reply_msg(msg,nickname+'走了，拜拜~')
