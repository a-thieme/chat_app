import socket

# Our header is 64 bytes
HEADER = 64

PORT = 5050

FORMAT = 'utf-8'

# This is the message that we send whenever we are ready to disconnect.
# Whenever this message is disconnected, the server will close the connection from said client.
DISCONNECT_MESSAGE = ".exit"

# This gets the local IPv4 address automatically without hard-coding it into the app
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

# This is the socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

# This will allow us to send messages
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(4096).decode(FORMAT))