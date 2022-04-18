import select
import socket
import threading

# Our header is 64 bytes
HEADER = 64

PORT = 5050

# This gets the local IPv4 address automatically without hard-coding it into the app
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

FORMAT = 'utf-8'

# This is the message that we send whenever we are ready to disconnect.
# Whenever this message is disconnected, the server will close the connection from said client.
DISCONNECT_MESSAGE = ".exit"

# This will generate a socket that will the server to connect to the client(s)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds the socket to the server address
server.bind(ADDR)

SOCKET_LIST = [server]


# Handles all communication between server and client
def handle_client(conn, addr):
    print(f"[NEW CONNECTIONS] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(FORMAT))

    conn.close()


# Starts the server socket and listens for connections and handles the connections and then passing them to
# handle_client()
def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("Welcome! Server is starting now!")
start()
