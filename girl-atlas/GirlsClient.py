from httpclient import HttpClient
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import config1
import os

GIRLS_URL = 'http://girl-atlas.com/'

class GirlsClient():
    def __init__(self, client):
        self._client = HttpClient(client)
        self._albumq = asyncio.Queue()
        self._photoq = asyncio.Queue()
        self._count = 0
        self._flag = False

    async def crawl_album_url(self):
        html = await self._client.get(GIRLS_URL)
        count = 1

        while True:
            soup = BeautifulSoup(html, 'html.parser')
            albums = soup.find_all('a', class_='caption')

            for album in albums:
                await self._albumq.put([album.attrs['href'], album.get_text()])

            next_page = soup.find_all('a', class_='btn-form next')
            if next_page == []:
                break

            html1 = await self._client.get(GIRLS_URL + next_page[0].attrs['href'])
            if html1 == None:
                continue
            else:
                html = html1

            print ()
            print ('已经下载完第 %s 页' % count)
            print ()
            count += 1

            await asyncio.sleep(config1.next_page_interval)

        await self._albumq.put(['111111', 'the end'])

    async def crawl_image_url(self):
        while True:
            [album_url, album_title] = await self._albumq.get()
            if album_url == 'the end':
                await self._photoq.put(['album_title', 'the end'])
                break

            html = await self._client.get(album_url)
            if html == None:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            photos = soup.find_all('li', class_='slide')
            if photos == []:
                continue

            for photo in photos:
                img = photo.find('img')
                title = img.attrs['title']
                try:
                    url = img.attrs['src']
                except:
                    url = img.attrs['delay']

                await self._photoq.put([album_title, url])

            await asyncio.sleep(config1.crawl_url_interval)

    async def download_image(self):
        if not os.path.exists('img'):
            os.makedirs('img')
        while True:
            [album_title, img_url] = await self._photoq.get()
            if img_url == 'the end':
                self._flag = True
            if album_title.find('|') != -1:
                index = album_title.find('|')
                album_title = album_title[:index]
            if not os.path.exists('img/' + album_title):
                print ()
                print ('生成文件夹：' + album_title)
                print ()
                os.makedirs('img/' + album_title)

            self._count += 1
            if (self._count % 10 == 0):
                print ('正在下载第 %s 张图片，%s' % (self._count, album_title))

            imgname = img_url.split('/')[-1][:-4]

            if os.path.exists('./img/' + album_title + '/' + imgname):
                print ('第 %s 张图片已经下载过，不重复下载。。。' % self._count)
                continue

            await self._client.downloadfile(img_url, './img/' + album_title + '/' + imgname)


            await asyncio.sleep(config1.download_interval)

    async def monitor(self):
        count = 1
        crawl_url_interval = config1.crawl_url_interval
        next_page_interval = config1.next_page_interval

        while True:
            print ()
            print ('目前下载队列还有：%s 个。' % self._photoq.qsize())
            print ()
            count += 1
            config1.crawl_url_interval = crawl_url_interval
            config1.next_page_interval = next_page_interval
            if count > 5:
                count = 1
                config1.crawl_url_interval = 40
                config1.next_page_interval = 20
                print ('让爬虫休息一下。。。')
                if self._flag == True:
                    print ('读取页面结束。。。。正在清空下载队列。。。。')
            await asyncio.sleep(20)
