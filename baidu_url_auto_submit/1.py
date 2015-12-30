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

def auto_ping(url):
    sitemap_url = 'http://www.lyyyuna.com/sitemap.xml'
    bing_ping = 'http://www.bing.com/webmaster/ping.aspx?siteMap=' + sitemap_url

    get = urllib2.urlopen(bing_ping)
    result = get.read()
    print result
    print


    ## import xml.etree.ElementTree as ET

    root = ET.Element("methodCall")
    methodname = ET.SubElement(root, "methodName").text = 'weblogUpdates.extendedPing'
    params = ET.SubElement(root, "params")


    param = ET.SubElement(params, "param")
    value = ET.SubElement(param, 'value')
    string = ET.SubElement(value, 'string').text = u'lyyyuna 的小花园'

    param = ET.SubElement(params, "param")
    value = ET.SubElement(param, 'value')
    string = ET.SubElement(value, 'string').text = u'http://www.lyyyuna.com/'

    param = ET.SubElement(params, "param")
    value = ET.SubElement(param, 'value')
    string = ET.SubElement(value, 'string').text = url

    param = ET.SubElement(params, "param")
    value = ET.SubElement(param, 'value')
    string = ET.SubElement(value, 'string').text = u'http://www.lyyyuna.com/atom.xml'

    # tree = ET.ElementTree(root)
    xmlstr = ET.tostring(root, encoding='utf8', method='xml')
    # print xmlstr
    # print

    baidu_pingRPC = 'http://ping.baidu.com/ping/RPC2'
    req = urllib2.Request(baidu_pingRPC, xmlstr)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page
    print



values = ''
new_blog_flag = False
new_blog_url = ''

loc_string = '{http://www.sitemaps.org/schemas/sitemap/0.9}loc'
for url in root:
    for attr in url:
        if attr.tag == loc_string:
            if not check_if_exist(attr.text):
                # print attr.text
                cur.execute("insert into urls (url) values ('" + attr.text + "')")
                values = values + attr.text + '\n'

                new_blog_flag = True
                new_blog_url = attr.text;

cx.commit()

print values

if new_blog_flag:
    auto_ping(new_blog_url)


baidu_zhanzhang_url = 'http://data.zz.baidu.com/urls?site=www.lyyyuna.com&token=XXXXXXXXXXXXXXXXXX&type=original'
# values = 'http://www.lyyyuna.com/2015/12/28/robotframework-quickstartguide/'

req = urllib2.Request(baidu_zhanzhang_url, values)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page