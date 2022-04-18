from common import *


def start():
    # This is the socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(".exit", client)


class Client(Yummy):
    def __init__(self):
        super().__init__()

    def callback(self, conn, message, addr=None):
        if message == DISCONNECT_MESSAGE:
            print('You have disconnected. Please press ENTER to finish.')
            return False
        print(f'{message}')
        return True

    def handle_connection(self, conn, addr=None):
        while True:
            try:
                message = receive(conn)
            except ConnectionResetError:
                break
            if message:
                if not self.callback(conn, message):
                    break
        exit()

    def listen(self):
        self.sock.connect(ADDR)
        t = threading.Thread(target=self.handle_connection, args=[self.sock])
        t.start()
        while True:
            try:
                out = input('')
                self.send(out)
            except ConnectionAbortedError:
                break
            except ValueError:
                break


if __name__ == '__main__':
    y = Client()
