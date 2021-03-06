# coding: utf-8
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

from smart_qq_bot.logger import logger
from smart_qq_bot.main import run
import smart_qq_bot.sqlite as sql
import json

db=r"./config/data.db"

if not os.path.exists(db):
    sql.connect(db)
    sql.execute('create table Manager(id integer primary key autoincrement unique not null,account_id varchar(20),group_id varvhar(20));')
    sql.execute('create table account_data(id integer primary key autoincrement unique not null,account_id varchar(20),account_code varvhar(20));')
    sql.execute('create table group_data(id integer primary key autoincrement unique not null,group_id varchar(20),group_name varchar(100),group_code varvhar(20));')
    sql.execute('create table discu_data(id integer primary key autoincrement unique not null,fake_did varchar(20),discu_name varvhar(100));')
    sql.execute("create table plugins(id integer primary key autoincrement unique not null,account varchar(20),plugin_name varchar(100),account_type varchar(20));")
    with open("./config/plugin.json","r") as f:
        t=f.read()
    plugins=json.load(t).get('plugin_on')
    managers=json.load(t).get('manager')
    for i in plugins:
        sql.execute("insert into plugins(account,plugin_name,account_type) values ('{0}','{1}','{2}');".format("00000",i,'group'))
    for i in managers:
        sql.execute("insert into Manager(account_id,group_id) values('{0}','{1}');".format(i,'00000'))
else:
    sql.connect(db)


try:
    run()
except KeyboardInterrupt:
    sql.close()
    logger.info("User stop. exit.")
    exit(0)