from common import *


def start():
    # This is the socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(".exit", client)


if __name__ == '__main__':
    start()
