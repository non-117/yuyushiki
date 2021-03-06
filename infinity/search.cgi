#! /usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import sqlite3
from functools import reduce
from jinja2 import Environment, FileSystemLoader 

conn = sqlite3.connect('yuyushiki.db', check_same_thread=False)

def search(word):
    sql = 'select path from comics where script like "%{0}%"'.format(word)
    cursor = conn.cursor()
    l = cursor.execute(sql).fetchall()
    cursor.close()
    if l == []:
        return l
    return reduce(lambda x, y: x+y,l)

def index():
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template('search.html')
    word = cgi.FieldStorage().getvalue('word')
    results = search(word)
    params = {'results':results,'count':len(results)}
    html = tpl.render(params)
    print('Content-Type: text/html; charset=utf-8\n')
    print(html.encode('utf-8'))

if __name__ == '__main__':
    index()

