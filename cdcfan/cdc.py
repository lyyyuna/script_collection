#! /usr/bin/python

def submitcdcfan():
    import sqlite3

    cx = sqlite3.connect("cdc.db3")
    cur = cx.cursor()
    cur.execute('select * from cdcuser');
    r = cur.fetchall()
    print r


    import urllib
    import urllib2
    import json
    import subprocess
    import os


#import datetime

#while True:
        #workday = datetime.date.today().weekday()
        #if (workday == 5 || workday == 6):
        #    continue

    for user in r:
        psid = user[2]
        depcode = user[3]
        email = user[4]

        post_data = {'order':'e-1', 'psid':psid, 'depcode':depcode}
        post_data_urlencode = urllib.urlencode(post_data)

        req_url = 'http://cdcfan/api/order-new'
        req = urllib2.Request(url = req_url, data = post_data_urlencode)

        res_data = urllib2.urlopen(req)
        res_json = res_data.read()
        print res_json

        res = json.loads(res_json)
        if (res['succeed_count'] == 0):
            cmd = "echo 'ding can shi bai, nin ke neng yi jing ding guo le. DO NOT REPLY' | mail -s cdcfanauto " + email
            # print cmd
            os.system(cmd)
        else:
            cmd = "echo 'ding can cheng gong. DO NOT REPLY' | mail -s cdcfanauto " + email
            os.system(cmd)


if __name__=='__main__':
    submitcdcfan()
