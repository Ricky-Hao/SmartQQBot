import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
from smart_qq_plugins.Nickname import REPLY_CONTENT,REPLY_SUFFIX
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message
import json

########################
plugin_name="Manager"
HELP={
    1:'Manager: 控制插件',
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
def isManager(msg,account_type):
    if account_type=='group':
        if sql.fetch_one('select * from Manager where account_id={0} and group_id={1};'.format(msg.send_uin,msg.group_id)):
            return True
        elif sql.fetch_one('select * from Manager where account_id={0} and group_id="00000";'.format(msg.send_uin)):
            return True
        else:
            return False
    else:
        return True
#######################

#######################

#######################
@on_all_message(name=plugin_name)
def Manager(msg,bot):
    #获取群号
    (account,account_type)=utils.get_account_and_type(msg)
    logger.debug('[Manager] account={0}, account_type={1}, send_uin={2}'.format(account,account_type,send_uin))
    logget.debug('[Manager] '+isManager(msg,account_type))
    if isManager(msg,account_type):
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
            logger.info('[Manager] '+account_type+': '+account+' Manager success')
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
                if close_plugin_name != 'Manager':
                    #从数据库中删除群号-插件关系
                    l=sql.fetch_all('select plugin_name from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
                    tmp=[]
                    for i in l:
                        tmp.append(i[0])
                    if close_plugin_name in tmp:
                        sql.execute("delete from plugins where account={0} and plugin_name='{1}' and account_type='{2}';".format(account,close_plugin_name,account_type))
                        logger.info('[Manager] '+account_type+': '+account+' inactivate '+close_plugin_name)
                        bot.reply_msg(msg,"关闭{0}插件成功~".format(close_plugin_name))
                    else:
                        bot.reply_msg(msg,close_plugin_name+'插件还没开启呢！')
                else:
                    bot.reply_msg(msg,'不能关闭Manager插件哦~')

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
                    logger.info('[Manager] '+account_type+': '+account+' Manager '+open_plugin_name)
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

            #添加管理人员
            elif account_type=='group' and utils.is_match(r'^!管理 add (\d{5,12})$',msg.content):
                manager_id=utils.is_match(r'^!管理 add (\d{5,12})$',msg.content).group(1)
                if sql.execute('select * from Manager where account_id={0} and group_id={1};'.format(manager_id,account)):
                    bot.reply_mag(msg,'已经是管理员啦~')
                else:
                    sql.execute('insert into Manager(account_id,group_id) values("{0}","{1}");'.format(manager_id,account))
                    bot.reply_msg(msg,"{0} 成功成为管理人员~".format(manager_id))

            #列出管理人员
            elif account_type=='group' and utils.is_match(r'^!管理 list$',msg.content):
                l=sql.fetch_all('select * from Manager where group_id={0};'.format(account))
                p=sql.fetch_all('select * from Manager where group_id="00000";')
                if l:
                    s='全局管理员：\n'
                    for i in p:
                        s+=i+'\n'
                    s+='群管理员：\n'
                    for i in l:
                        s+=i+'\n'
                    bot.reply_msg(msg,s)
                else:
                    bot.reply_msg(msg,"没有管理人员哦~")

            #删除管理人员
            elif account_type=='group' and utils.is_match(r'^!管理 remove (\d{5,12})$',msg.content):
                manager_id=utils.is_match(r'^!管理 remove (\d{5,12})$',msg.content).group(1)
                sql.execute('delete from Manager where account_id={0} and group_id={1};'.format(manager_id,account))
                bot.reply_msg(msg,'{0} 已不再是管理员。。。'.format(manager_id))


            #完全关闭
            elif utils.is_match(r'^!回去吧 (.*)$',msg.content):
                m_nickname=utils.is_match(r'^!回去吧 (.*)$',msg.content).group(1)
                nickname=sql.fetch_one('select nickname from Nickname where account="{0}" and account_type="{1}";'.format(account,account_type))[0]
                if m_nickname==nickname:
                    sql.execute('delete from plugins where account="{0}" and account_type="{1}";'.format(account,account_type))
                    bot.reply_msg(msg,nickname+'走了，拜拜~')
