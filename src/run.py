# coding: utf-8
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

from smart_qq_bot.logger import logger
from smart_qq_bot.main import run
import sqlite3
import json

db=r"./config/data.db"

if not os.path.exists(db):
    con = sqlite3.connect(db)
    con.execute("create table uin_plugins(id integer primary key autoincrement unique not null,uin varchar(20),plugin_name varchar(100));")
    con.execute("create table if not exists basic(id integer primary key autoincrement unique not null, nickname varchar(100), uin varchar(20), content varchar(20));")
    name="test"
    with open("./config/plugin.json","r") as f:
         plugins=json.load(f).get('plugin_on')
    for i in plugins:
        con.execute("insert into uin_plugins(uin,plugin_name) values (?,?);",("00000",i))
    con.execute("insert into basic(uin,nickname,content) values (?,?,?);",("00000",name,"test"))
    con.commit()
    con.close()
else:
    con=sqlite3.connect(db)

try:
    run()
except KeyboardInterrupt:
    logger.info("User stop. exit.")
    exit(0)