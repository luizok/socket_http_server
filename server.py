from tcp_server import TCPServer
import os


HOST = '0.0.0.0'
PORT = 8080


class HTTPServer(TCPServer):

    def handle_request(self, req, client):

        req_path = req.decode('utf-8').split('\r\n')[0]
        method, path, _ = req_path.split(' ')

        print('[*] {} -> SERVER: {} {}'.format(client, method, path))

        if path == '/':
            path += 'index.html'

        path = os.path.join(os.getcwd(), path[1:])

        if not os.path.isfile(path):
            return bytes(''.join((
                'HTTP/1.1 404 Not Found\r\n',
                '\r\n'
            )), 'utf-8')

        res = None
        if path.endswith('html'):
            res = self.parse_text(method, path)
        elif path.endswith('ico'):
            res = self.parse_binary(method, path)

        return res

    def parse_text(self, method, path):

        content = ''
        with open(path, 'r', encoding='utf-8') as fd:
            content = ''.join(fd.readlines())

        content = bytes(content, 'utf-8')
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

    def parse_binary(self, method, path):

        content = b''
        with open(path, 'rb') as fd:
            byte = fd.read(4096)
            while byte:
                content += byte
                byte = fd.read(4096)

        header = bytes(''.join([
                'HTTP/1.1 200 OK\r\n',
                'Server: ScratchServer\r\n',
                'content-Type: image/ico\r\n',
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
