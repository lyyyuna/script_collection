# -*- coding:utf-8 -*-
import sys
import urllib
# sys.setdefaultencoding('utf-8')

home_id = 5441
player_url = "http://live.bilibili.com/api/player?id=cid:" + str(home_id)
f=urllib.urlopen(player_url)
s=f.read()
print s


import socket
#from socket import *
bilibili_host = 'livecmt-1.bilibili.com'
port = 88
bilibili_ip = socket.gethostbyname('livecmt-1.bilibili.com')
print bilibili_ip
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((bilibili_ip, port))

from struct import *
send_bytes = pack('!BBBBII',1,1,0,12,home_id,0)
s.sendall(send_bytes)
data_binary = s.recv(555)

import binascii
num_people = binascii.b2a_hex(data_binary)
num_people = num_people[4:]
print int(num_people, 16)

send_bytes = pack('!BBBB',1,2,0,4)
s.sendall(send_bytes)
data_binary = s.recv(555)
num_people = binascii.b2a_hex(data_binary)
num_people = num_people[4:]
print int(num_people, 16)



import json

while True:



    buf = s.recv(1024)
    if len(buf) == 0:
        pass

    buf = buf[4:]
    json_buf = str(buf)

    try:
        j = json.loads(json_buf)
    except ValueError:
        continue
        

    CMD = j['cmd']
    if CMD == 'DANMU_MSG':
        words = j['info'][1].encode('utf8')
        # print words
        user = j['info'][2][1].encode('utf8')
        print user, 'say:', words

s.close()