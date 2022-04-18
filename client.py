from common import *


def start():
    # This is the socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(".exit", client)




class Client(Yummy):
    def __init__(self):
        super().__init__()

    def handle_connection(self, conn, addr=None):
        friends = ['SERVER']
        while True:
            try:
                message = receive(conn)
            except ConnectionResetError:
                break
            if message:
                if message == DISCONNECT_MESSAGE:
                    print('You have disconnected. Please press ENTER to finish.')
                    break
                if '[SERVER]: You are now talking' in message:
                    message = message.replace('[SERVER]', '').replace("'", '').split(' [')[1].split(']')[0]
                    friends = ['SERVER'] + (message.split(', '))
                    print(f'friends: {friends}')
                if message.startswith('['):
                    sender_id = message.split('[')[1].split(']')[0]
                    print(f'friends: {friends}')
                    print(f'send id: {sender_id}')
                    if sender_id in friends:
                        print(f'{message}')
                    else:
                        print(f'{sender_id} wants to talk....')

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
