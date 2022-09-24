import socket
from time import sleep
from json import dumps, loads


class Client:
    def __init__(self, host, port, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.id = '{}:{}'.format(self.socket.getsockname()[0], self.socket.getsockname()[1])


    def receive(self):
        return self.socket.recv(1024).decode()

    def send(self, message):
        self.socket.send(message.encode())

    def close(self):
        self.socket.close()


class ChatClient (Client):
    def __init__(self, host, port, buffer_size=1024):
        super().__init__(host, port, buffer_size)
        self.connect()
        self.connected_room = None
        
    def create_package(self, package_type, data, target_room_id=None):
        """Create a package
            Ex: {type: 'message', sender_id: 'ip:port', data: 'Hello world!, target_room_id: 1}
        """
        package = {
            'type': package_type,
            'data': data,
            'sender_id': self.id,
            'sender_username': self.username,
            'target_room_id': self.connected_room if target_room_id == None else target_room_id
        }
        return dumps(package)

    def parse_package(self, package):
        """Parse a package"""
        return loads(package)

    def configure_client(self, username):
        self.username = username

    def wait_for_response(self):
        recieved_package = ''
        while True:
            recieved_package = self.receive()
            if recieved_package:
                return self.parse_package(recieved_package)
            sleep(0.3)
    
    def join_room(self):
        selected_room = input('Enter the desired room: ')
        self.send(self.create_package('join_room', None, selected_room))
        self.connected_room = selected_room
            
    def disconnect(self):
        self.send(self.create_package('disconnect', None))
        self.close()
