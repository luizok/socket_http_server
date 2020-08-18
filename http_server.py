from tcp_server import TCPServerConcurrent
import os


class HTTPServer(TCPServerConcurrent):

    def __init__(self, host='127.0.0.1', port=8080):
        super().__init__(host, port)
        self.status_code = {
            100: 'Continue',
            101: 'Switching Protocols',
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            307: 'Temporary Redirect',
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Time-out',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Request Entity Too Large',
            414: 'Request-URI Too Large',
            415: 'Unsupported Media Type',
            416: 'Requested range not satisfiable',
            417: 'Expectation Failed',
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Time-out',
            505: 'HTTP Version not supported'
        }

    def build_response(self, http_v=1.1, code=200, content=None, headers={}):

        res = ''
        res += 'HTTP/{} '.format(http_v)
        res += '{} {}\r\n'.format(code, self.status_code[code])

        for k, v in headers.items():
            res += '{}: {}\r\n'.format(k, v)

        res += '\r\n'
        res = bytes(res, 'utf-8')

        if content:
            res += content

        return res

    def handle_request(self, req, client):

        req_path = req.decode('utf-8').split('\r\n')[0]
        method, path, _ = req_path.split(' ')

        print('[*] {} -> SERVER: {} {}'.format(client, method, path))

        if method == 'GET':
            if path == '/':
                path += 'index.html'

            path = os.path.join(os.getcwd(), path[1:])

            if not os.path.isfile(path):
                return self.build_response(code=404, headers={
                    'Server': 'ScratchServer',
                    'Content-Type': 'text/html; charset=utf-8',
                    'Content-Length': '0',
                })

            res = None
            ext = path.split('.')[-1]
            if ext in ('html', 'txt'):
                res = self.parse_text(method, path)
            elif ext in ('ico', 'jpg', 'jpeg', 'png'):
                res = self.parse_binary(method, path)

            return res

        return self.build_response(code=405, headers={
            'Server': 'ScratchServer',
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Length': '0',
        })

    def parse_text(self, method, path):

        content = ''
        with open(path, 'r', encoding='utf-8') as fd:
            content = ''.join(fd.readlines())
        content = bytes(content, 'utf-8')

        res = self.build_response(code=200, content=content, headers={
            'Server': 'ScratchServer',
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Length': str(len(content)),
        })

        return res

    def parse_binary(self, method, path):

        content = b''
        with open(path, 'rb') as fd:
            byte = fd.read(4096)
            while byte:
                content += byte
                byte = fd.read(4096)

        res = self.build_response(code=200, content=content, headers={
            'Server': 'ScratchServer',
            'Content-Type': 'image/ico',
            'Content-Length': str(len(content)),
        })

        return res