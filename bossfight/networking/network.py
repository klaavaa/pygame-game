import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.0.11'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.c = self.connect()

    def get_c(self):
        return self.c

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(f'error: {e}')

    def request(self):
        return pickle.loads(self.client.recv(2048))


