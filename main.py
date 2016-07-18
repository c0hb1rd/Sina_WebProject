#!/usr/bin/env python
# coding=utf-8
from flask import Flask
import MySQLdb as mysql

app = Flask(__name__)

dbConn = mysql.connect('localhost', 'root', 'hackingme?233333+1s', 'test')
cursor = dbConn.cursor()
cursor.execute('SELECT * FROM user')
data = cursor.fetchall()
columns = [i[0] for i in cursor.description]

@app.route('/')
def index():
    return str(columns)

app.debug = True
app.run(host='0.0.0.0')
