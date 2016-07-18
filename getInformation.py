#!/usr/bin/env python
# coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup

HEADERS_FOR_GET_INFO = {
    'Cookie':'wb_bub_hot_5447809712=1; SINAGLOBAL=738129014972.3884.1468458217951; wb_g_minivideo_5447809712=1; UOR=,,drops.wooyun.org; YF-V5-G0=a53c7b4a43414d07adb73f0238a7972e; YF-Ugrow-G0=b02489d329584fca03ad6347fc915997; WBStore=8ca40a3ef06ad7b2|undefined; _s_tentry=-; Apache=7005031656669.645.1468824575977; ULV=1468824575981:2:2:1:7005031656669.645.1468824575977:1468458217966; WBtopGlobal_register_version=80ab5a863737bcd5; SCF=AsZPw5rkbPDnnKWKR1i3EMxVD2eXvWt_SHHKeyYZnOVHv_y6jaWVEe15Z2Tgu3qhaYCdUFYed5JJZPrdw3hAb1g.; SUB=_2A256iAxaDeTxGeNK71UZ8CfLyj6IHXVZ_HqSrDV8PUNbmtBeLVqskW8Tu_lwu5FxkTrBZA6fF7kleD7CaA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWlXurN77AppfK3I6VNbye25JpX5K2hUgL.Fo-XShMReh.NeKz2dJLoIpjLxK-LBonLB-BLxK-L1hML12eLxK-LBo5LBKqt; SUHB=0ftZl1zJuRht__; ALF=1469429385; SSOLoginState=1468824586; un=13729545205; wvr=6; YF-Page-G0=f017d20b1081f0a1606831bba19e407b'
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
