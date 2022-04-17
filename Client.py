import socket
from threading import Thread


class Client:
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('localhost', port))
        # # make a thread that listens for messages to this client & print them
        # t = Thread(target=self.listen_for_messages)
        # # make the thread daemon so it ends whenever the main thread ends
        # t.daemon = True
        # # start the thread
        # t.start()

    def start(self):
        # todo: these need to be threaded
        self.send('init', self.s)
        self.listen_for_messages(self.s)
        self.send_loop(self.s)

    def listen_for_messages(self, s):
        # listens for messages from the server and prints them to the console
        message = 'placeholder'
        out = []
        while message != '':
            message = s.recv(1024).decode('utf-8')
            out.append(message)
        message = ''.join(out)
        print("\n" + message)
        if message == 'END':
            self.close()
        elif message.startswith('connection'):
            # connection port
            new_socket = "port at " + message.split(' ')[1]
            self.listen_for_messages(new_socket)
            self.send_loop(new_socket)

    def send_loop(self, sock):
        while True:
            sock.send(input('send message: '))

    def send(self, message, s):
        message = message.encode('utf-8')
        s.send(message)

    def close(self):
        self.s.close()
