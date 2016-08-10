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
    sql.execute('create table group_data(id integer primary key autoincrement unique not null,group_id varchar(20),group_name varchar(100),group_code varvhar(20));')
    #sql.execute('create table private_data(id integer primary key autoincrement unique not null,private_id varchar(20),private_code varvhar(20));')
    sql.execute("create table plugins_group(id integer primary key autoincrement unique not null,group_id varchar(20),plugin_name varchar(100));")
    sql.execute("create table plugins_private(id integer primary key autoincrement unique not null,private_id varchar(20),plugin_name varchar(100));")
    with open("./config/plugin.json","r") as f:
         plugins=json.load(f).get('plugin_on')
    for i in plugins:
        sql.execute("insert into plugins_group(group_id,plugin_name) values ('{0}','{1}');".format("00000",i))
        sql.execute("insert into plugins_private(private_id,plugin_name) values ('{0}','{1}');".format("00000",i))
else:
    sql.connect(db)

try:
    run()
except KeyboardInterrupt:
    sql.close()
    logger.info("User stop. exit.")
    exit(0)