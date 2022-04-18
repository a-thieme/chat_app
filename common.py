import socket

# all of our global variables that both client and server use

PORT = 5050
# Our header is 64 bytes
HEADER = 64
FORMAT = 'utf-8'

# This gets the local IPv4 address automatically without hard-coding it into the app
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

# This is the message that we send whenever we are ready to disconnect.
# Whenever this message is disconnected, the server will close the connection from said client.
DISCONNECT_MESSAGE = ".exit"


# static send message on X connection
def send(msg, sock):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    sock.send(send_length)
    sock.send(message)


# static receive message on X connection
def receive(sock):
    msg_length = sock.recv(HEADER).decode()
    if msg_length:
        msg_length = int(msg_length)
        msg = sock.recv(msg_length).decode(FORMAT)
        return msg


# base networking class for client and server
class Yummy:
    def __init__(self):
        # generation of a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # listen is really like the "run" function
        self.listen()

    # send wrapper
    def send(self, msg, s=None):
        # send message on personal socket if none is given (client)
        if s is None:
            send(msg, self.sock)
        # send message on given socket (server)
        else:
            send(msg, s)

    # these are the basic functions to be implemented/overridden by client and server, but idk if I used callback

    # run self
    def listen(self):
        return

    # for any connection, this has the logic for it
    def handle_connection(self, conn, addr=None):

        return

    # for any message, this will be the logic for the message (maybe unused)
    def callback(self, conn, message, addr=None):

        return
