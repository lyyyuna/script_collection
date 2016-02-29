import asyncio
import aiohttp
from GirlsClient import GirlsClient


with aiohttp.ClientSession() as client:
    girls = GirlsClient(client)

    tasks = [
            girls.crawl_album_url() ,
            girls.crawl_image_url() ,
            girls.download_image() ,
            girls.download_image() ,
            girls.download_image() ,
            girls.monitor()
            ]

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
