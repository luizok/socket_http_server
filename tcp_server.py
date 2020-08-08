import socket
import sys


class TCPServer:

    def __init__(self, host='127.0.0.1', port=8080):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))

    def start(self):
        self.s.listen(0)
        print('[*] Server listening at {}'.format(
            self.s.getsockname()
        ))

        while True:
            conn, client = self.s.accept()
            print('[*] {} -> SERVER: New Connection'.format(client))

            while True:
                data = conn.recv(1024)

                if not data: break
                print('[*] {} -> SERVER: Request received'.format(client))
                res = '<html><header><title>PAGE</title><header><body>My Response</body></html>'

                try:
                    n = conn.sendto(bytes(''.join((
                        'HTTP/1.1 200 OK\r\n',
                        'Server: FromScratchServer\r\n',
                        'Content-Type: text/html\r\n',
                        'Content-Length: ' + str(len(bytes(res, 'utf-8'))) + '\r\n',
                        '\r\n',
                        res
                        )), 'utf-8'), 0, client)
                    print('[*] SERVER -> {}: Sent {} bytes'.format(client, n))
                except Exception as e:
                    print(e)
                    server.close()
                    sys.exit(-1)
            
            print('[*] SERVER -> {}: Ending connection'.format(client))
    
    def close(self):
        self.s.close()