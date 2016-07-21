#!/usr/bin/env python
# coding=utf-8
import MySQLdb as mysql
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests
import sys
from bs4 import BeautifulSoup
import os
import json
import time

reload(sys)
sys.setdefaultencoding('utf-8')


HEADERS_FOR_GET_INFO = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'',
    'Host':'m.weibo.cn',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

def getUserInformation(uid, headers=HEADERS_FOR_GET_INFO):
    url = "http://m.weibo.cn/users/%d?retcode=6102" % int(uid)
    reponse = requests.get(url, headers=HEADERS_FOR_GET_INFO)
    reponse.close()

    content = BeautifulSoup(reponse.content.replace("\\", '').replace("rn", ""), "html.parser")
    content = content.find_all('div', 'item-info-page')

    info = {}
    for v in content:
        key = str(v.find('span'))[6:-7]
        value = str(v.find('p'))[3:-4]
        if key == '备注':
            continue
        elif key == '勋章':
            continue
        elif key[-12:] == '微博认证':
            key = key[-12:]
        info[key] = value.decode('utf-8')
    info['UID'] = int(uid)

    return info

def getImageLinks(uid, page, headers=HEADERS_FOR_GET_INFO):
    uid = int(uid)
    while True:
        try:
            imgLinks = []

            content = ''
            url = "http://m.weibo.cn/page/json?containerid=103003index%d_-_photo_all_l&page=%d" % (uid, page)
            reponse = requests.get(url, headers=headers)
            reponse.close()

            if reponse:
                content = reponse.content.replace('\\', '')
            data = json.loads(content)

            print data['count']
            if data['count'] < 2 or data['count'] == '':
                return None

            for src in data['cards'][0]['card_group'][0]['pics']:
                imgLinks.append(src['pic_ori'].replace('large', 'thumb300')) # Large Type Picture is too Big

            return imgLinks
        except:
            continue


# Get User Fans Total, Return Int
def getUserFans(uid, headers=HEADERS_FOR_GET_INFO):
    uid = int(uid)
    while True:
        try:
            url = "http://m.weibo.cn/page/card?itemid=100505%d_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102" % uid
            reponse = requests.get(url, headers=headers)
            reponse.close()

            content = reponse.content.replace('\\', '')
            data = json.loads(content[17:-1])
            fans = data['apps'][3]['count'].split('u')

            if len(fans) > 1:
                if fans[1] == '4ebf':
                    totalFans = fans[0] + '00000000'
                    return int(totalFans)
                elif fans[1] == '4e07':
                    totalFans = fans[0] + '0000'
                    return int(totalFans)
            else:
                return int(fans[0])
        except:
            continue


app = Flask(__name__)

dbConn = mysql.connect('localhost', 'root', '', 'sina_spider')
cursor = dbConn.cursor()
cursor.execute("SET NAMES UTF8")
cursor.execute('SELECT * FROM user')
datas = cursor.fetchall()
test = datas[0][3].decode('utf-8')
columns = [i[0] for i in cursor.description]

#2640810462
@app.route('/', methods=['GET'])
def index():
    uid = request.args.get('uid')
    page = int(request.args.get('page'))
    data = getUserInformation(uid)
    fans = getUserFans(uid)
    data['粉丝'] = fans
    imgLinks1 = getImageLinks(uid, page)
    imgLinks2 = getImageLinks(uid, page + 1)
    imgLinks3 = getImageLinks(uid, page + 2)
    imgLinks4 = getImageLinks(uid, page + 3)
    imgLinks5 = getImageLinks(uid, page + 4)
    imgLinks = imgLinks1 + imgLinks2 + imgLinks3 + imgLinks4 + imgLinks5
    return render_template('show.html', imgLinks=imgLinks, data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print 'hello'
    else:
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


app.debug = True
app.run(host='0.0.0.0')
