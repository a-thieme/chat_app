import pandas as pd
from Server import Server
from Client import Client


def do_client(port):
    print('client initialize')
    client = Client(port)
    print('client send')
    data = [['Alex', 10], ['Bob', 12], ['Clarke', 13]]
    df = pd.DataFrame(data, columns=['Name', 'Age'])
    mess = df.to_json()
    # client.send('test message')
    client.send(mess)
    client.close()


def do_server(port):
    server = Server(port)
    server.run()


def main():
    port = 17001
    do_server(port)


if __name__ == '__main__':
    main()
