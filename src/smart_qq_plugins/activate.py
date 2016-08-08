import sqlite3
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_all_message, on_bot_inited
import json

REPLY_CONTENT=(
    "干嘛（‘·д·）",
    "嗯",
    "肿么了",
    "在呀",
    "不约",
    "嗯哼",
    "啊哈"
)

@on_all_message(name="activate")
def activate(msg,bot):
    if msg.content.rfind("!召唤 ")==0:
        name=msg.content[4:]
        con = sqlite3.connect("./config/data.db")
        if len(con.execute('select * from basic where uin="{0}";'.format(str(msg.from_uin))).fetchall())==0:
            with open("./config/plugin.json","r") as f:
                plugins=json.load(f).get('plugin_on')
            for i in plugins:
                con.execute("insert into uin_plugins(uin,plugin_name) values (?,?);",(msg.from_uin,i))
            for i in REPLY_CONTENT:
                con.execute("insert into basic(uin,nickname,content) values (?,?,?);",(msg.from_uin,name,i))
            con.commit()
            con.close()
            bot.reply_msg(msg,"召唤{0}成功~".format(name))
        else:
            bot.reply_msg(msg,"已经召唤过{0}啦~".format(name))
    if msg.content.rfind("!关闭 ")==0:
        con = sqlite3.connect("./config/data.db")
        plugin_name=msg.content[4:]
        con.execute("delete from uin_plugins where uin={0} and plugin_name={1};".format(str(msg.from_uin),plugin_name))
        con.commit()
        con.close()
        bot.reply_msg(msg,"关闭{0}插件成功~".format(plugin_name))
    if msg.content.rfind("!开启 ")==0:
        con = sqlite3.connect("./config/data.db")
        plugin_name=msg.content[4:]
        con.execute("insert into uin_plugins(uin,plugin_name) values (?,?);",(msg.from_uin,plugin_name))
        con.commit()
        con.close()
        bot.reply_msg(msg,"开启{0}插件成功~".format(plugin_name))
    if msg.content.rfind("!已启用插件")==0:
        con = sqlite3.connect("./config/data.db")
        cur=con.cursor()
        cur.execute('select plugin_name from uin_plugins where uin="{0}";'.format(str(msg.from_uin)))
        l=cur.fetchall()
        s="已启用插件：\n"
        for i in l:
            s+=i[0]+'\n'
        con.close()
        bot.reply_msg(msg,s)
