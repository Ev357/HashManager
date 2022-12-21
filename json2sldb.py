#!/usr/bin/python3
import sqlite3 as sl, os, json

fcd = os.path.dirname(os.path.realpath(__file__)) + '/'
data = json.load(open(fcd + './data.json'))

conn = None
try:
    conn = sl.connect(fcd + "./db/out.db")
except sl.Error as e:
    print(e)
    exit()
    if conn:
        conn.close()

sql = 'CREATE TABLE IF NOT EXISTS data (username TEXT, hash TEXT, password TEXT, state BOOLEAN);'
cur = conn.cursor()
cur.execute(sql)
conn.commit()

for _ in data:
    if _["state"] == 1:
        sql = f'INSERT INTO data (username, hash, password, state) VALUES("{_["username"]}", "{_["hash"]}", "{_["password"]}", {str(_["state"])});'
    else:
        sql = f'INSERT INTO data (username, hash, password, state) VALUES("{_["username"]}", "{_["hash"]}", "", {str(_["state"])});'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
