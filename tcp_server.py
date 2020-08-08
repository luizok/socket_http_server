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

                res = self.handle_request(data, client)

                try:
                    n = conn.sendto(res, 0, client)
                    print('[*] SERVER -> {}: Sent {} bytes'.format(client, n))
                except Exception as e:
                    print(e)
                    server.close()
                    sys.exit(-1)
            
            print('[*] SERVER -> {}: Ending connection'.format(client))
    
    # Override by subclasses
    def handle_request(self, req, client):
        res = ''
        return res

    def close(self):
        self.s.close()