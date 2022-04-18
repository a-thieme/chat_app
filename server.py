import select
import socket
import threading
import time

from random import randint

from common import *

conns_dict = {'-1': ''}


class Server(Yummy):
    def __init__(self):
        super().__init__()

    def listen(self):
        self.sock.bind(ADDR)
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thread.start()

    def create_id(self):
        r = -1
        x = 2
        while r < 1 or str(r) in conns_dict:
            r = randint(0, x)
            x *= 2
        return str(r)

    def send_list(self):
        for person in conns_dict:
            if person == '-1':
                continue
            tmp = ''
            for key in conns_dict:
                if key != person:
                    tmp += str(key) + '\n'
            if tmp != '':
                self.send(f'[SERVER]: Updated available connections as IDs:\n{tmp}', conns_dict[person])

    def handle_connection(self, conn, addr=None):
        print(f"[NEW CONNECTIONS] {addr} connected.")
        conn_id = self.create_id()
        conns_dict[conn_id] = conn
        print(f'[ID GENERATED]: {conn_id} for {addr}')
        self.send(f'[SERVER]: Your ID is {conn_id}.', conn)
        self.send('[SERVER]: To make a new connection, use "add <id>"\nTo remove an existing connection, use "del <id>.\nTo '
                  'exit, enter ".exit"', conn)
        self.send('[SERVER]: ID -1 is the chat room', conn)
        self.send_list()
        talking_to = []
        while True:
            try:
                message = receive(conn)
            except ConnectionResetError:
                break
            if message:
                if message == DISCONNECT_MESSAGE:
                    try:
                        send(DISCONNECT_MESSAGE, conn)
                        del conns_dict[conn_id]
                        print(f'[CONNECTION REMOVED]: {conn_id}')
                        self.send_list()
                        conn.close()
                    except:
                        'placeholder'
                    break
                if message.startswith('add '):
                    maybe = message.split('add ')[1]
                    if maybe in conns_dict:
                        talking_to.append(maybe)
                        self.send(f'[SERVER]: You are now talking in/to ID(s) {talking_to}.', conn)
                    else:
                        self.send('[SERVER]: twas not a valid ID', conn)
                elif message.startswith('del '):
                    maybe = message.split('del ')[1]
                    if maybe in talking_to:
                        talking_to.remove(maybe)
                        self.send(f'[SERVER]: You are now talking in/to ID(s) {talking_to}.', conn)
                    else:
                        self.send('[SERVER]: twas not a valid ID', conn)
                else:
                    for person in talking_to:
                        if person != '-1':
                            try:
                                self.send(f'[{conn_id}]:\t{message}', conns_dict[person])
                            except KeyError:
                                talking_to.remove(person)
                        else:
                            print('person was n1')
                            for user in conns_dict:
                                if user != '-1' and user != conn_id:
                                    self.send(f'[-1][{conn_id}]:\t{message}', conns_dict[user])

                    if len(talking_to) == 0:
                        self.send('[SERVER]: maybe try adding a connection before trying to send a message', conn)


if __name__ == '__main__':
    print("Welcome! Server is starting now!")
    # start()
    Server()
