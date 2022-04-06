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

    def listen_for_messages(self):
        # listens for messages from the server and prints them to the console
        while True:
            message = self.s.recv(1024).decode()
            print("\n" + message)

    def send(self, message):
        message = message.encode('utf-8')
        self.s.send(message)

    def close(self):
        self.s.close()
