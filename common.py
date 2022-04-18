import socket
import threading

# Our header is 64 bytes
PORT = 5050
HEADER = 64
FORMAT = 'utf-8'

# This gets the local IPv4 address automatically without hard-coding it into the app
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

# This is the message that we send whenever we are ready to disconnect.
# Whenever this message is disconnected, the server will close the connection from said client.
DISCONNECT_MESSAGE = ".exit"


def send(msg, sock):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sock.send(send_length)
    sock.send(message)


def receive(sock):
    msg_length = sock.recv(HEADER).decode()
    if msg_length:
        msg_length = int(msg_length)
        msg = sock.recv(msg_length).decode(FORMAT)
        return msg


class Yummy:
    def __init__(self):
        # generation of a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(ADDR)

    def listen(self):
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thread.start()

    def handle_connection(self, conn, addr):
        connected = True
        while connected:
            response = receive(conn)
            if response:
                if response == DISCONNECT_MESSAGE:
                    conn.close()
                    connected = False
                else:
                    self.callback(conn, addr)

    def callback(self, conn, addr):

        return

