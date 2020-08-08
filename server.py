import socket


HOST = '0.0.0.0'
PORT = 8080


if __name__ == '__main__':

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        
        print('[*] Ending connection with {}'.format(client))
        conn.close()

