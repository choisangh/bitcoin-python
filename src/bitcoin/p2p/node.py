import socket
import pickle


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.blocks = []

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)

        print("Node started on {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024)

            if not data:
                continue

            message = pickle.loads(data)

            if message['type'] == 'block':
                block = message['block']
                self.blocks.append(block)
                print("Block received from {}:{}".format(client_address[0], client_address[1]))
                print("Block Hash: ", block['hash'])

            client_socket.close()

    def send_block(self, host, port, block):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        message = {'type': 'block', 'block': block}
        data = pickle.dumps(message)

        client_socket.send(data)
        client_socket.close()


if __name__ == '__main__':
    node1 = Node('localhost', 5000)
    node2 = Node('localhost', 5001)

    # Start Node1
    node1.start()

    # Start Node2
    node2.start()

    # Node1 sends block to Node2
    block = {'hash': '00000000000000000000000000000001', 'data': 'Block Data'}
    node1.send_block('localhost', 5001, block)