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
    'Cookie':'_T_WM=353f92d15219ad271f0706ec5441d2a6; ALF=1471416585; SCF=AsZPw5rkbPDnnKWKR1i3EMxVD2eXvWt_SHHKeyYZnOVHE-B96mB4FLZYbaWwYpwsrGr6U_6vxKDy6OPDvvneqkw.; SUB=_2A256iPOyDeTxGeNK71UZ8CfLyj6IHXVWcp36rDV6PUJbktBeLRCjkW2fTiNq47Ohrg3VNMNivNZd9Erlbw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWlXurN77AppfK3I6VNbye25JpX5o2p5NHD95QfShBN1h54S02EWs4Dqcjdi--fi-zRi-82i--fiKnNiKyhi--fi-z7i-2c; SUHB=08JLK0nzY-Ap65; SSOLoginState=1468826594; gsid_CTandWM=4ur5CpOz5RpQ6Noj0exA9mRdTbu',
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
            url = "http://m.weibo.cn/page/json?containerid=103003index%d_-_photo_all_l&page=%d&retcode=6102" % (uid, page)
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


app = Flask(__name__)

dbConn = mysql.connect('localhost', 'root', 'hackingme?233333+1s', 'sina_spider')
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
    imgLinks1 = getImageLinks(uid, page)
    imgLinks2 = getImageLinks(uid, page + 1)
    imgLinks3 = getImageLinks(uid, page + 2)
    imgLinks = imgLinks1 + imgLinks2 + imgLinks3
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
