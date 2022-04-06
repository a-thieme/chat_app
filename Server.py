import socket
from threading import Thread


def deal_with_client(c_sock):
    out = []
    r = 'placeholder'
    segments = 1
    while r != '':
        r = c_sock.recv(4000)
        r = r.decode('utf-8')
        out.append(r)
        segments += 1

    print(''.join(out))
    print(f'segments={segments}')


class Server:
    def __init__(self, port, connections=5):
        self.thread = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))
        self.s.listen(connections)

    def server_loop(self):
        while True:
            c_sock, addr = self.s.accept()
            t = Thread(target=deal_with_client(c_sock))
            t.run()

    def run(self):
        self.thread = Thread(target=self.server_loop())
        self.thread.run()
