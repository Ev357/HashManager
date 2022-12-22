#!/usr/bin/python3
import sqlite3 as sl, os, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output file name', default='out.db', action="store")
required = parser.add_argument_group('required arguments')
required.add_argument('-i', '--input', help='Input file name', required=True, action="store")
parser._action_groups.reverse()
args = parser.parse_args()

fcd = os.path.dirname(os.path.realpath(__file__)) + '/'
data = json.load(open(fcd + args.input))

conn = None
try:
    conn = sl.connect(fcd + args.output)
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
