# coding=utf-8

import asyncio
import aiohttp
import json

class HttpClient:
    def __init__(self, client):
        self._client = client

    async def get(self, url, params=None):
        try:
            async with await self._client.get(url, params=params) as r:
                return await r.text()
        except :
            return None

    async def downloadfile(self, url, filename):
        try:
            with aiohttp.Timeout(3):
                async with await self._client.get(url) as r:
                    with open(filename, 'wb') as fd:
                        while True:
                            chunk = await r.content.read(4096)
                            if not chunk:
                                break
                            fd.write(chunk)
                    return True
        except:
            return False
