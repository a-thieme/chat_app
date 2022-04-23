from random import randint
from common import *
import threading

conns_dict = {'-1': ''}
keys = {}


# create unique id that is greater than 0
def create_id():
    r = -1
    x = 2
    while r < 1 or str(r) in conns_dict:
        r = randint(0, x)
        x *= 2
    return str(r)


class Server(Yummy):
    def __init__(self):
        super().__init__()

    def listen(self):
        # bind server port and listen on it
        self.sock.bind(ADDR)
        self.sock.listen()
        while True:
            # on any new connection, run the handle_connection code
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thread.start()

    # sends list of users to every connection (other than chat room)
    def send_list(self):
        for person in conns_dict:
            if person == '-1':
                continue
            tmp = ''
            for key in conns_dict:
                # don't send the user its own id
                if key != person:
                    tmp += str(key) + '\n'
            if tmp != '':
                self.send(f'[SERVER]: Updated available connections as IDs:\n{tmp}', conns_dict[person])

    def send_keys(self):
        for person in conns_dict:
            if person == '-1':
                continue
            for key in keys:
                if key != person:
                    self.send(f'[SERVER][KEY] {key}:{keys[key]}', conns_dict[person])

    # server logic for every individual connection/user
    def handle_connection(self, conn, addr=None):
        print(f"[NEW CONNECTIONS] {addr} connected.")
        # create unique id
        conn_id = create_id()
        # add id: connection to conns_dict
        conns_dict[conn_id] = conn
        print(f'[ID GENERATED]: {conn_id} for {addr}')
        # send user its given ID
        self.send(f'[SERVER]: Your ID is {conn_id}.', conn)
        self.send(f'[SERVER][DH] {PRIME}:{ROOT}', conn)
        # send a "help/readme" message
        self.send('[SERVER]: To make a new connection, use "add <id>"\n[SERVER]: To remove an existing connection, '
                  'use "del '
                  '<id>.\n[SERVER]: To '
                  'exit, enter ".exit"', conn)
        self.send('[SERVER]: ID -1 is the chat room', conn)
        # send updated connection list to every user
        self.send_list()
        # talking_to is a list of names of your "friends" aka the connections you've added
        talking_to = []
        # listening loop for client
        while True:
            # if connection broke, stop the loop
            try:
                message = receive(conn)
            except ConnectionResetError:
                break
            if message:
                # on
                if message == DISCONNECT_MESSAGE:
                    # on disconnect message, send it back to terminate client side program
                    try:
                        send(DISCONNECT_MESSAGE, conn)
                        # also remove connection from the list of available connections
                        del conns_dict[conn_id]
                        print(f'[CONNECTION REMOVED]: {conn_id}')
                        # send updated list of connections
                        self.send_list()
                        conn.close()
                    # many things might not work
                    except:
                        'placeholder'
                    break
                # adding a connection
                if message.startswith('[KEY]: '):
                    tmp = message.replace('[KEY]: ', '')
                    keys[conn_id] = tmp
                    print(keys)
                    self.send_keys()
                elif message.startswith('add '):
                    # maybe is just the id that we think they wanted to add
                    maybe = message.split('add ')[1]
                    if maybe in conns_dict:
                        # add connection if it's valid, but dupes don't get added twice
                        talking_to.append(maybe)
                        talking_to = list(set(talking_to))
                        # send client their "friend list"
                        self.send(f'[SERVER]: You are now talking in/to ID(s) {talking_to}.', conn)
                    else:
                        # error if id not found
                        self.send('[SERVER]: twas not a valid ID', conn)
                # same as adding but it deletes
                elif message.startswith('del '):
                    maybe = message.split('del ')[1]
                    if maybe in talking_to:
                        talking_to.remove(maybe)
                        self.send(f'[SERVER]: You are now talking in/to ID(s) {talking_to}.', conn)
                    else:
                        self.send('[SERVER]: twas not a valid ID', conn)
                else:
                    try:
                        send_to = message.split('[')[1].split(']')[0]
                    except:
                        break
                    message = message.split('\t')[1]
                    # broadcast message to everyone you're talking to
                    if send_to in talking_to:
                        if send_to != '-1':
                            # for all people, send them message with [your-id] at the beginning
                            try:
                                self.send(f'[{conn_id}]:\t{message}', conns_dict[send_to])
                            # sometimes users aren't removed when they disconnect, so this handles that
                            except KeyError:
                                talking_to.remove(send_to)
                        # you're sending to chat room
                        else:
                            # send to every person in connections other than yourself
                            for user in conns_dict:
                                if user != '-1' and user != conn_id:
                                    self.send(f'[-1][{conn_id}]:\t{message}', conns_dict[user])

                    # you have no friends
                    if len(talking_to) == 0:
                        self.send('[SERVER]: maybe try adding a connection before trying to send a message', conn)


if __name__ == '__main__':
    print("Welcome! Server is starting now!")
    Server()
