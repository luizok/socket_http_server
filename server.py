import socket
import sys


HOST = '0.0.0.0'
PORT = 8080


if __name__ == '__main__':

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind((HOST, PORT))
    tcp.listen(1)

    print('[*] {} Listening on port {}'.format(HOST, PORT))

    while True:
        conn, client = tcp.accept()
        print('[*] new connection from {}'.format(client))

        while True:
            data = conn.recv(512)

            if not data: break
            print('[*] {} says {}'.format(client, data))

            try:
                n = conn.sendto(bytes(''.join((
                    'HTTP/1.1 200 OK\r\n',
                    'Content-Type: text/html\r\n'
                    '\r\n',
                    'Reponse'
                    )), 'utf-8'), 0, client)
                print(conn)
                print('Sent {} bytes'.format(n))
            except Exception as e:
                print(e)
                tcp.close()
                sys.exit(-1)
        
        print('[*] Ending connection with {}'.format(client))
        conn.close()

