# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import urllib

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        uri = self.path
        # print uri
        proto, rest = urllib.splittype(uri)
        host, rest = urllib.splithost(rest)
        # print host
        path = rest        
        host, port = urllib.splitnport(host)
        if port < 0:
            port = 80
        print host
        host_ip = socket.gethostbyname(host)
        print port

        del self.headers['Proxy-Connection']
        self.headers['Connection'] = 'close'

        send_data = 'GET ' + path + ' ' + self.protocol_version + '\r\n'
        head = ''
        for key, val in self.headers.items():
            head = head + "%s: %s\r\n" % (key, val)
        send_data = send_data + head + '\r\n'
        # print send_data
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.connect((host_ip, port))
        so.sendall(send_data)

        # 因为采用非长连接，所以会关闭连接， recv 会退出
        data = ''
        while True:
             tmp = so.recv(4096)
             if not tmp:
                 break
             data = data + tmp

        # socprint data
        so.close()

        self.wfile.write(data)


    # do_CONNECT = do_GET

def main():
    try:
        server = HTTPServer(('', 8888), MyHandler)
        print 'Welcome to the machine...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()