import socket
from threading import Thread
import pandas as pd


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


def example_function(i=1):
    print('I am doing a thing')
    print('Now I am doing another thing')
    print(f'now I shall display the argument i {i} and its default value is 1 if you don\'t pass any value to it')


class Client:

    def listen_for_messages(self):
        # listens for messages from the server and prints them to the console
        while True:
            message = self.s.recv(1024).decode()
            print("\n" + message)
    # make a thread that listens for messages to this client & print them
    t = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('localhost', port))

    def send(self, message):
        message = message.encode('utf-8')
        self.s.send(message)

    def close(self):
        self.s.close()


def main():
    port = 17001
    print('client initialize')
    client = Client(port)
    print('client send')
    data = [['Alex', 10], ['Bob', 12], ['Clarke', 13]]
    df = pd.DataFrame(data, columns=['Name', 'Age'])
    mess = df.to_json()
    # client.send('test message')
    client.send(mess)
    client.close()


if __name__ == '__main__':
    main()
