# -*- coding: utf-8 -*-

import urllib
import urllib2


sitemap_url = 'http://www.lyyyuna.com/sitemap.xml'
get = urllib2.urlopen(sitemap_url)
xml_string = get.read()

import sqlite3
import xml.etree.ElementTree as ET
root = ET.fromstring(xml_string)

cx = sqlite3.connect('sitemap.db3')
cur = cx.cursor()
cur.execute('select * from urls')
all_urls = cur.fetchall()
# print all_urls[0][1]

def check_if_exist(url):
    for cached_url in all_urls:
        ascii_cached_url = cached_url[1].encode('ascii')
        # print ascii_cached_url
        if url == ascii_cached_url:
            return True

    return False

values = ''
loc_string = '{http://www.sitemaps.org/schemas/sitemap/0.9}loc'
for url in root:
    for attr in url:
        if attr.tag == loc_string:
            if not check_if_exist(attr.text):
                # print attr.text
                cur.execute("insert into urls (url) values ('" + attr.text + "')")
                values = values + attr.text + '\n'

cx.commit()

print values

baidu_zhanzhang_url = 'http://data.zz.baidu.com/urls?site=www.lyyyuna.com&token=XXXXXXXXXXXXXXXXXX&type=original'
# values = 'http://www.lyyyuna.com/2015/12/28/robotframework-quickstartguide/'

req = urllib2.Request(baidu_zhanzhang_url, values)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page