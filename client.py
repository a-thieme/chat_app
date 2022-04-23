from common import *
import threading


def start():
    # This is the socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(".exit", client)


class Client(Yummy):
    def __init__(self):
        super().__init__()

    # client just has one listening loop since it's only one connection to the server
    def handle_connection(self, conn, addr=None):
        # friends are the people who you are ok with seeing messages from
        friends = ['SERVER']
        while True:
            try:
                message = receive(conn)
            except ConnectionResetError:
                # this happens if/when the server closes a connection
                # the break just stops the listening
                # I don't know if this is necessary, but I know it works like this
                break
            # if message exists
            if message:
                # disconnect messages come from the server
                if message == DISCONNECT_MESSAGE:
                    print('You have disconnected. Please press ENTER to finish.')
                    break
                # checks for if the server sent back a list of the connections you've added
                if '[SERVER]: You are now talking in/to ID(s)' in message:
                    print(message)
                    # formatted with [id, id, id] at the end of the line
                    # gets just the id, id, id
                    message = message.replace('[SERVER]', '').replace("'", '').split(' [')[1].split(']')[0]
                    # updates friendly users based on the connections the server says we've made
                    friends = ['SERVER'] + (message.split(', '))
                # # everything should start with [id]
                else:
                    # this gets the id of the connection sending the message
                    sender_id = message.split('[')[1].split(']')[0]
                    # if the id was one we added, it'll show message, otherwise say that user wants to talk
                    if sender_id in friends:
                        print(message)
                    else:
                        print(f'{sender_id} wants to talk....')

        # ends this thread after loop is done
        exit()

    def listen(self):
        # connects to server
        self.sock.connect(ADDR)
        # runs listening in the background
        t = threading.Thread(target=self.handle_connection, args=[self.sock])
        t.start()
        # user input that sends to server
        # breaks on bad connections (connection was stopped by server)
        while True:
            try:
                out = input('')
                self.send(out)
            except ConnectionAbortedError:
                break
            except BrokenPipeError:
                break
            except ValueError:
                break


if __name__ == '__main__':
    print("Welcome to the ChatApp!")
    Client()
