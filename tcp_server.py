import socket
import sys
from threading import Thread
import logging


logging.basicConfig(
    level=logging.INFO,
    filename='server_log.log',
    filemode='a',
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


class TCPServer:

    def __init__(self, host='127.0.0.1', port=8080):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.log = logging.info

    def start(self):
        self.s.listen(0)
        print('[*] Server listening at {}'.format(self.s.getsockname()))
        self.log('Server listening at {}'.format(self.s.getsockname()))

        while True:
            conn, client = self.s.accept()
            print('[*] {} -> SERVER: New Connection'.format(client))
            self.log('{} -> SERVER: New Connection'.format(client))

            self.handle_new_client(conn, client)
    
    # Override by subclasses
    def handle_new_client(self, conn, client):
        return

    # Override by subclasses
    def handle_request(self, req, client):
        return

    def close(self):
        self.s.close()


class TCPServerSingle(TCPServer):

    def handle_new_client(self, conn, client):
        while True:
            data = conn.recv(1024)
            if not data: break

            res = self.handle_request(data, client)

            try:
                n = conn.sendto(res, 0, client)
                print('[*] SERVER -> {}: Sent {} bytes'.format(client, n))
                self.log('SERVER -> {}: Sent {} bytes'.format(client, n))
            except Exception as e:
                print(e)
                self.conn.close()
                sys.exit(-1)

        print('[*] SERVER -> {}: Ending connection'.format(client))
        self.log('SERVER -> {}: Ending connection'.format(client))


class ClientThread(Thread):

    def __init__(self, conn, client, server):
        super().__init__()
        self.conn = conn
        self.client = client
        self.handle_request = server.handle_request
        self.log = server.log

    def run(self):
        while True:
            data = self.conn.recv(1024)
            if not data: break

            res = self.handle_request(data, self.client)

            try:
                n = self.conn.sendto(res, 0, self.client)
                print('[*] SERVER -> {}: Sent {} bytes'.format(self.client, n))
                self.log('SERVER -> {}: Sent {} bytes'.format(self.client, n))
            except Exception as e:
                print(e)
                self.conn.close()

        print('[*] SERVER -> {}: Ending connection'.format(self.client))
        self.log('SERVER -> {}: Ending connection'.format(self.client))


class TCPServerConcurrent(TCPServer):

    def handle_new_client(self, conn, client):
        t = ClientThread(conn, client, self)
        t.start()
