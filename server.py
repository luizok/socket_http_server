from tcp_server import TCPServer
from pprint import pprint


HOST = '0.0.0.0'
PORT = 8080


class HTTPServer(TCPServer):

    def handle_request(self, req, client):

        req_path = req.decode('utf-8').split('\r\n')[0]
        method, path, _ = req_path.split(' ')

        print('[*] {} -> SERVER: {} {}'.format(client, method, path))

        content = bytes(
            '<html><header><title>PAGE</title><header><body>Site á b ó ô</body></html>',
            'utf-8'
        )
        header = bytes(''.join([
                'HTTP/1.1 200 OK\r\n',
                'Server: ScratchServer\r\n',
                'Content-Type: text/html; charset=utf-8\r\n',
                'Content-Length: ' + str(len(content)) + '\r\n',
                '\r\n'
            ]),
            'utf-8'
        )

        res = header + content
        return res


if __name__ == '__main__':

    server = HTTPServer()
    server.start()
