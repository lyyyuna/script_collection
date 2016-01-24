# coding=utf-8

import urllib2
import urllib
import ssl
import time
from cookielib import CookieJar

import re
import os
import xml.dom.minidom
import json

QRImagePath = os.path.join(os.getcwd(), 'qr_tmp.jpg')
uuid = ''
tip = 0

deviceID = 'e328624296179709'


def getRequest(url, data):
    try:
        data = data.encode('utf-8')
    except:
        pass
    finally:
        return urllib2.Request(url, data)

def getUUID():
    global uuid

    login_url = 'https://login.weixin.qq.com/jslogin'
    params = {
        'appid' : 'wx782c26e4c19acffb',
        'fun' : 'new',
        'lang' : 'zh_CN',
        '_' : int(time.time())
    }

    request = getRequest(login_url, urllib.urlencode(params))
    response = urllib2.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, data)

    code = pm.group(1)
    uuid = pm.group(2)

    if code == '200':
        return True
    return False


def showQRImage():
    global uuid 

    url = 'https://login.weixin.qq.com/qrcode/' + uuid
    params = {
        't' : 'webwx',
        '_' : int(time.time())
    }
    request = getRequest(url, urllib.urlencode(params))
    response = urllib2.urlopen(request)

    with open(QRImagePath, 'wb') as f:
        f.write(response.read())
        os.startfile(QRImagePath)
        tip = 1

    print 'scan the QR image please'


def wait_for_login():
    global tip, uuid, base_uri, redirect_uri

    url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
        tip, uuid, int(time.time()))

    request = getRequest(url, None)
    response = urllib2.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    regx = r'window.code=(\d+);'
    pm = re.search(regx, data)
    code = pm.group(1)

    if code == '201':
        print 'have scanned successfully, please press OK'
    elif code == '200':
        print 'logining ........'
        regx = r'window.redirect_uri="(\S+?)";'
        pm = re.search(regx, data)
        redirect_uri = pm.group(1) + '&fun=new'
        base_uri = redirect_uri[:redirect_uri.rfind('/')]
    else:
        print code
    return code


def login_test():
    global redirect_uri, skey, wxsid, wxuin, pass_ticket, base_request

    request = getRequest(redirect_uri, None)
    response = urllib2.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    dom_doc = xml.dom.minidom.parseString(data)
    root = dom_doc.documentElement

    for node in root.childNodes:
        if node.nodeName == 'skey':
            skey = node.childNodes[0].data 
        elif node.nodeName == 'wxsid':
            wxsid = node.childNodes[0].data 
        elif node.nodeName == 'wxuin':
            wxuin = node.childNodes[0].data 
        elif node.nodeName == 'pass_ticket':
            pass_ticket = node.childNodes[0].data

    # print skey, wxsid, wxuin, pass_ticket

    if not all((skey, wxsid, wxuin, pass_ticket)):
        return False

    base_request = {
        'Uin' : int (wxuin), 
        'Sid' : wxsid,
        'Skey' : skey,
        'DeviceID' : deviceID
    }

    return True


def weixin_init():
    global ContactList, User, SyncKeyList, SyncKey

    uri = base_uri + '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (pass_ticket, skey, int(time.time()))
    params = {'BaseRequest' : base_request}

    request = getRequest(uri, json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    dic = json.loads(data)
    ContactList = dic['ContactList']
    User = dic['User']

    SyncKeyList = []
    for item in dic['SyncKey']['List']:
        SyncKeyList.append('%s_%s' % (item['Key'], item['Val']))
    SyncKey = '|'.join(SyncKeyList)
    print dic['SyncKey']

    ErrMsg = dic['BaseResponse']['ErrMsg']

    Ret = dic['BaseResponse']['Ret']
    #print dic['BaseResponse']
    if Ret != 0:
        return False

    return True


def webwxstatusnotify():
    uri = base_uri  + '/webwxstatusnotify?lang=zh_CN&pass_ticket=%s' % pass_ticket
    params = {
        'BaseRequest' : base_request ,
        
    }

def sync_check():

    uri = 'https://webpush.weixin.qq.com/cgi-bin/mmwebwx-bin/synccheck?'
    params = {
        'skey': base_request['Skey'],
        'sid': base_request['Sid'],
        'uin': base_request['Uin'],
        'deviceid': base_request['DeviceID'],
        'synckey': SyncKey,
        'r': int(time.time()),
        '_': int(time.time())+1111  
    }

    print uri+urllib.urlencode(params)
    request = getRequest(uri + urllib.urlencode(params), None)
    response = urllib2.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    print data
    if data is not 'window.synccheck={retcode:"0",selector:"0"}':
        return True
    else:
        return False

def get_msg():

    uri = base_uri + '/webwxsync?sid=%s&skey=%s&pass_ticket=%s' % (wxsid, skey, pass_ticket)
    print 'test'

def auto_answer():
    if sync_check() is True:
        pass
    else:
        pass


def webwxgetcontact():

    uri = base_uri + '/webwxgetcontact?lang=zh_CN&pass_ticket=%s&skey=%s&seq=0&r=%s' % (pass_ticket, skey, int(time.time()))

    print uri
    request = getRequest(uri, None)
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    data = response.read()

    # if DEBUG:
    #     f = open(os.path.join(os.getcwd(), 'webwxgetcontact.json'), 'wb')
    #     f.write(data)
    #     f.close()

    print data
    data = data.decode('utf-8', 'replace')

    dic = json.loads(data)
    MemberList = dic['MemberList']

    
    SpecialUsers = ["newsapp", "fmessage", "filehelper", "weibo", "qqmail", "tmessage", "qmessage", "qqsync", "floatbottle", "lbsapp", "shakeapp", "medianote", "qqfriend", "readerapp", "blogapp", "facebookapp", "masssendapp",
                    "meishiapp", "feedsapp", "voip", "blogappweixin", "weixin", "brandsessionholder", "weixinreminder", "wxid_novlwrv3lqwv11", "gh_22b87fa7cb3c", "officialaccounts", "notification_messages", "wxitil", "userexperience_alarm"]
    for i in range(len(MemberList) - 1, -1, -1):
        Member = MemberList[i]
        if Member['VerifyFlag'] & 8 != 0:  # 公众号/服务号
            MemberList.remove(Member)
        elif Member['UserName'] in SpecialUsers:  # 特殊账号
            MemberList.remove(Member)
        elif Member['UserName'] == My['UserName']:  # 自己
            MemberList.remove(Member)

    return MemberList




def main():

    # ssl._create_default_https_context = ssl._create_unverified_context
    # openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))
    # urllib2.install_opener(openner)

    if not getUUID():
        print 'fail to get uuid'

    showQRImage()
    while wait_for_login() != '200':
        pass
    os.remove(QRImagePath)

    if not login_test():
        print 'fail to login'
        return

    if not weixin_init():
        print 'fail to init'
        return 

    time.sleep(1)
    print webwxgetcontact()
    # try:
    #     while True:
    #         auto_answer()
    # except KeyboardInterrupt:
    #     print 'exit'

if __name__ == '__main__':
    main()