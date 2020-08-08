from tcp_server import TCPServer
import sys


HOST = '0.0.0.0'
PORT = 8080


if __name__ == '__main__':

    server = TCPServer(HOST, PORT)
    server.start()

