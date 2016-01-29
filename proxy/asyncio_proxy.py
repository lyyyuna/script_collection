# -*- coding: utf-8 -*-

from urllib.parse import urlparse, parse_qsl

import aiohttp
import aiohttp.server
import asyncio

class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
    def __init__(self):
        super().__init__()

    async def handle_request(self, message, payload):
        url = message.path
        url_parsed = urlparse(url)
        # print (url_parsed)
        print (url)
        if message.method == 'GET':
            headers = message.headers
            if 'Proxy-Connection' in headers:
                del headers['Proxy-Connection']
            headers['Connection'] = 'close'
            response = await aiohttp.request('GET', url, headers=headers)

            await self.send_msg(response)


    async def send_msg(self, response):
        proxy_response = aiohttp.Response(self.writer, response.status, http_version=response.version)
        # Do not pass on Content-Encoding header to client.
        # Unfortunately aiohttp transparently decodes content, so sending any Content-Encoding header to the client would be incorrect.
        proxy_response_headers = [
            (name, value) for name, value
            in response.headers.items()
            if name not in ('CONTENT-ENCODING')
        ]

        proxy_response.add_headers(*proxy_response_headers)
        proxy_response.send_headers()

        response_content = response.content
        while True:
            chunk = await response_content.read(512)
            if not chunk:
                break
            proxy_response.write(chunk)
        await proxy_response.write_eof()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    f = loop.create_server(
        lambda: HttpRequestHandler(), '0.0.0.0', '8880'
    )
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
