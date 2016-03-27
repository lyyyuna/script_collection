import fcntl
import os
import asyncio

class asyncfile:
    BLOCK_SIZE = 512

    def __init__(self, filename, mode, loop=None):
        self.fd = open(filename, mode=mode)
        flag = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        if fcntl.fcntl(self.fd, fcntl.F_SETFL, flag | os.O_NONBLOCK) != 0:
            raise OSError()

        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.rbuffer = bytearray()

    def read_step(self, future, n, total):

        res = self.fd.read(n)

        if res is None:
            self.loop.call_soon(self.read_step, future, n, total)
            return
        if not res: # EOF
            future.set_result(bytes(self.rbuffer))
            return

        self.rbuffer.extend(res)

        if total > 0:
            left = total - len(self.rbuffer)
            print (left)
            if left <= 0:
                # res, self.rbuffer = self.rbuffer[:n], self.rbuffer[n:]
                future.set_result(bytes(self.rbuffer))
            else:
                left = min(self.BLOCK_SIZE, left)
                self.loop.call_soon(self.read_step, future, left, total)
        else:
            self.loop.call_soon(self.read_step, future, self.BLOCK_SIZE, total)

    def read(self, n=-1):
        future = asyncio.Future(loop=self.loop)

        if n == 0:
            future.set_result(b'')
            return future
        elif n < 0:
            self.rbuffer.clear()
            self.loop.call_soon(self.read_step, future, self.BLOCK_SIZE, n)
        else:
            self.rbuffer.clear()
            self.loop.call_soon(self.read_step, future, min(self.BLOCK_SIZE, n), n)

        return future

async def test():

    af = asyncfile('pp.py', mode='rb')
    content = await af.read(8000)
    print (content)

if __name__ == '__main__':

    tasks = [test()]
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
