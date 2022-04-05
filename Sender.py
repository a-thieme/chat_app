from Main import Client

if __name__ == '__main__':
    port = 17001
    print('client initialize')
    client = Client(port)
    print('client send')
    client.send(str([i for i in range(100000)]))

    client.close()
