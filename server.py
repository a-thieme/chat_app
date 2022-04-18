import select
import socket
import threading
from common import *


SOCKET_LIST = []


# Handles all communication between server and client
def handle_client(conn, addr):
    print(f"[NEW CONNECTIONS] {addr} connected.")

    connected = True
    while connected:
        response = receive(conn)
        if response:
            if response == DISCONNECT_MESSAGE:
                connected = False
            print(response)

    conn.close()


# Starts the server socket and listens for connections and handles the connections and then passing them to
# handle_client()
def start():
    # This will generate a socket that will the server to connect to the client(s)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binds the socket to the server address
    server.bind(ADDR)
    SOCKET_LIST.append(server)

    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == '__main__':
    print("Welcome! Server is starting now!")
    start()
