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
