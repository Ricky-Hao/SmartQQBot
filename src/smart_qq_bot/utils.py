import re
import smart_qq_bot.sqlite as sql

def in_plugins(account,account_type,plugin_name):
    return sql.fetch_one('select * from plugins where account="{0}" and account_type="{1}" and plugin_name="{2}";'.format(account,account_type,plugin_name))

def is_match(p,s):
    return re.match(p,s)

def check_table(name):
    return sql.fetch_all('select count(*) from sqlite_master where type="table" and name="{0}";'.format(name))[0][0] != 0
    
def get_account_and_type(msg):
    if msg.type=="group_message":
        account_type='group'
        account=msg.group_id
    elif msg.type=="message":
        account_type='private'
        account=msg.private_id
    elif msg.type=="discu_message:
        account_type='discu'
        account=msg.fake_did
    else:
        account="0"
        account_type="None"
    return (account,account_type)