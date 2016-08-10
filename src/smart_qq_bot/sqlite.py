import sqlite3



def connect(s):
    global con
    con=sqlite3.connect(s,check_same_thread=False)

def close():
    global con
    con.close()

def execute(s):
    global con
    con.execute(s)
    con.commit()

def fetch_one(s):
    global con
    return con.execute(s).fetchone()

def fetch_all(s):
    global con
    return con.execute(s).fetchall()

def get_private_id(name):
    global con
    #从 plugins_private表 中提取启用了该插件的 QQ号 数据，并以列表的形式储存在private_id
    tmp=con.execute('select private_id from plugins_private where plugin_name="{0}";'.format(name)).fetchall()
    private_id=[]
    for i in tmp:
        private_id.append(i[0])
    return private_id

def get_group_id(name):
    global con
    #从 plugins_group表 中提取启用了该插件的 群号 数据，并以列表形式储存在group_id
    tmp=con.execute('select group_id from plugins_group where plugin_name="{0}";'.format(name)).fetchall()
    group_id=[]
    for i in tmp:
        group_id.append(i[0])
    return group_id

def check_table(name):
    global con
    return con.execute('select count(*) from sqlite_master where type="table" and name="{0}";'.format(name)).fetchall()[0][0] != 0

