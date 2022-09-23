import socket
from time import sleep

class Client:
    def __init__(self, host, port, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def receive(self):
        return self.socket.recv(1024).decode()

    def send(self, message):
        self.socket.send(message.encode())

    def close(self):
        self.socket.close()

    def wait_for_response(self):
        while True:
            response = self.receive()
            if response:
                return response
            sleep(0.3)