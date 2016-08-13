import smart_qq_bot.sqlite as sql
import smart_qq_bot.utils as utils
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message,on_bot_inited
from collections import OrderedDict
import json
import os
import sys

plugin_name="Help"
HELP={
    'Help':'帮助列表插件',
    '帮助 插件名':'获取相应插件的Help文件'
}

def update_help_data():
    with open("./config/plugin.json",'r') as f:
        plugin_list=json.load(f).get('plugin_on')
    for p in plugin_list:
        if not sql.fetch_one('select help from Help where plugin_name="{0}";'.format(p)):
            try:
                tmp=(__import__('smart_qq_plugins.'+p,fromlist=['HELP']))
                logger.debug(tmp)
                sql.execute("insert into Help(plugin_name,help) values('{0}','{1}');".format(p,json.dumps(tmp.HELP))) 
            except Exception as e:
                logger.debug(e)
        
        
def help_init():
    if not utils.check_table('Help'):
        sql.execute('create table Help(id integer primary key autoincrement unique not null,plugin_name varchar(100),help varchar(1000));')

help_init()
update_help_data()

@on_all_message(name=plugin_name)
def Help(msg,bot):
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugin_name):
        if utils.is_match(r'^(帮助|Help|help) (.*)$',msg.content):
            help_plugin_name=utils.is_match(r'^(帮助|Help|help) (.*)$',msg.content).group(2)
            with open('./plugin.json''r') as f:
                plugin_list=json.load(f).get('plugin_on')
            if help_plugin_name not in plugin_list:
                bot.reply_msg(msg,'没有这个插件啦~')
            else:
                if sql.fetch_one('select * from Help where plugin_name="{0}";'.format(help_plugin_name)):
                    help_content=json.loads(sql.fetch_one('select help from Help where plugin_name="{0}";'.format(help_plugin_name))[0],object_pairs_hook=OrderedDict)
                    s=""
                    for k in help_content.keys():
                        s+=k+'  '+help_content[k]+'\n'
                    bot.reply_msg(msg,s)
                else:
                    bot.reply_msg(msg,'这个插件还暂时没有帮助文件哦！')
