import time

from common import *
import threading


def start():
    # This is the socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(".exit", client)


class Client(Yummy):
    secret = None
    prime = None
    keys = {}
    def __init__(self):
        super().__init__()

    def send_encrypted(self, msg, sending_to):
        msg_bits = msg.encode(FORMAT)
        nonce = 152
        key = self.keys[sending_to].to_bytes(BLOCK_SIZE, 'big')
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce.to_bytes(BLOCK_SIZE, 'big'))
        out = str(cipher.encrypt(msg_bits), FORMAT)
        self.send(f'[{sending_to}]\t{out}')

    # client just has one listening loop since it's only one connection to the server
    def handle_connection(self, conn, addr=None):
        # friends are the people who you are ok with seeing messages from
        friends = ['SERVER']
        while True:
            try:
                message = receive(conn)
                nonce = 152
                incoming = message.split('[')[1].split(']')[0]
                if incoming in self.keys:
                    key = self.keys[incoming].to_bytes(BLOCK_SIZE, 'big')
                    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce.to_bytes(BLOCK_SIZE, 'big'))
                    if ']:\t' in message:
                        print(f'{message}\t(encrypted)')
                        both = message.split(']:\t')
                        head = both[0] + ']:\t'
                        rest = both[1]
                        rest = cipher.decrypt(bytes(rest, FORMAT)).decode(FORMAT)
                        message = head + rest + ' (decrypted)'
            except ConnectionResetError:
                # this happens if/when the server closes a connection
                # the break just stops the listening
                # I don't know if this is necessary, but I know it works like this
                break
            except:
                break
            # if message exists
            if message:
                # disconnect messages come from the server
                if message == DISCONNECT_MESSAGE:
                    print('You have disconnected. Please press ENTER to finish.')
                    break
                # checks for if the server sent back a list of the connections you've added
                if '[SERVER]: You are now talking in/to ID(s)' in message:
                    # formatted with [id, id, id] at the end of the line
                    # gets just the id, id, id
                    tmp = message.replace('[SERVER]', '').replace("'", '').split(' [')[1].split(']')[0]
                    # updates friendly users based on the connections the server says we've made
                    friends = ['SERVER'] + (tmp.split(', '))
                # this gets the id of the connection sending the message
                sender_id = message.split('[')[1].split(']')[0]
                # if the id was one we added, it'll show message, otherwise say that user wants to talk
                if '[SERVER][DH] ' in message:
                    tmp = message.split(' ')[1]
                    prime, root = tmp.split(':')
                    prime = int(prime)
                    root = int(root)
                    self.secret = randint(1, prime)
                    self.send(f'[KEY]: {(root ** self.secret) % prime}')
                    self.prime = prime
                elif '[SERVER][KEY] ' in message:
                    eyedee, key = message.split(' ')[1].split(':')
                    key = int(key)
                    key = (key ** self.secret) % self.prime
                    self.keys[eyedee] = key
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
        time.sleep(0.5)
        while True:
            try:
                connection = input('')
                if '.exit' in connection:
                    self.send('.exit')
                    break
                out = input('')
                if '.exit' in out:
                    self.send('.exit')
                    break
                if connection == 'server' or connection == '-1':
                    self.send(out)
                else:
                    if connection in self.keys:
                        self.send_encrypted(out, connection)
                    else:
                        print(f'did not find key for {connection}')
            except ConnectionAbortedError:
                break
            except BrokenPipeError:
                break
            except ValueError:
                break
            except:
                break


if __name__ == '__main__':
    print("Welcome to the ChatApp!")
    print("Enter 'server' or any connection, press enter, then type your message you want to send and press enter again to send it.")
    Client()
