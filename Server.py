import socket
from threading import Thread


class Connection:
    def __init__(self, username, out_port):
        self.socket = socket
        self.out_port = out_port
        self.username = username


class Server:
    # dict of connections with key being the username
    current_conns = {}

    def __init__(self, port, connections=5):
        self.thread = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))
        self.s.listen(connections)

    # main server loop to get incoming connections on main port
    def server_loop(self):
        while True:
            c_sock, addr = self.s.accept()
            t = Thread(target=self.deal_with_client(c_sock))
            t.run()

    def run(self):
        self.thread = Thread(target=self.server_loop())
        self.thread.run()

    # client uses this
    def request(self, client_a, client_b):
        # api for client a to use to try to connect with client b
        return

    # server uses this
    def handle_request_connection(self, client_a, client_b):
        # client A requests to chat with client B
        # if client B confirms, assign new sockets
        return

    # internal server forwarding
    def run_connection(self, client_a, client_b):
        # should be threaded operation to send all messages from a to b and all from b to a given ports
        message = 'recieved message'
        response = ''
        client_a.send('END')
        if message == 'END':
            client_a.disconnect()

        client_a.send('END')
        if response == 'okay':
            client_b.disconnect()
        return

    def deal_with_client(self, c_sock):
        out = []
        r = 'placeholder'
        while r != '':
            r = c_sock.recv(4000)
            r = r.decode('utf-8')
            out.append(r)
        message = ''.join(out)
        print(self.current_conns)
        # sending usernames
        if message == ('init' or 'users'):
            c_sock.send(str(self.current_conns.keys).encode('utf-8'))
        if message in self.current_conns:
            self.handle_request_connection('a','b')
        # getting supplied username and storing
        r = 'place'
        out = []
        while r != '':
            r = c_sock.recv(1024).decode('utf-8')
            out.append(r)
        self.current_conns[''.join(out)] = c_sock

