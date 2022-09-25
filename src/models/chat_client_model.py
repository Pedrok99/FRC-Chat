import socket
from time import sleep
from json import dumps, loads
from select import select
from sys import stdin


class Client:
    def __init__(self, host, port, buffer_size=1024):
        self.server_host = host
        self.server_port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.server_host, self.server_port))
        self.ip = self.socket.getsockname()[0]
        self.port = self.socket.getsockname()[1]
        self.id = '{}:{}'.format(self.ip, self.port)

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
        self.available_commands = {
            '/commands': 'Show available commands',
            '/rooms': 'Show all rooms',
            '/join': 'Join a room',
            '/leave': 'Leave the current room',
            '/quit': 'Quit the chat app'
        }

    # package managment methods
    def create_package(self, package_type, data, target_room_id=None):
        """Create a package
            Ex: {type: 'message', sender_id: 'ip:port', data: 'Hello world!, target_room_id: 1}
        """
        package = {
            'type': package_type,
            'data': data,
            'sender_id': self.id,
            'sender_username': '{}#{}'.format(self.username, self.port),
            'target_room_id': self.connected_room if target_room_id == None else target_room_id
        }
        return dumps(package)

    def parse_package(self, package):
        """Parse a package"""
        return loads(package)
    # remove method later

    def configure_client(self, username):
        self.username = username

    # commands methods - /commands
    def show_commands(self):
        print('Commands:')
        for command, description in self.available_commands.items():
            print('  {} - {}'.format(command, description))

    # commands methods - /join
    def join_room(self):
        selected_room = input('Enter the desired room: ')
        self.send(self.create_package('join_room', None, selected_room))
        self.connected_room = selected_room

    # command method - /rooms
    def list_rooms(self):
        request_package = self.create_package('list_rooms', None)
        self.send(request_package)
    
    # command method - /leave
    def leave_room(self):
        self.send(self.create_package('leave_room', None ))
        self.connected_room = None
        
    def create_room(self, room_name, limit):
        self.send(self.create_package('create_room', {'room_name': room_name, 'limit': limit}))
    

    # command method - /quit
    def disconnect(self):
        self.send(self.create_package('disconnect', None))
        self.close()
        
    
    # chat methods
    def send_message(self, message):
        """Send a package to the server"""
        self.send(self.create_package('message', message))

    # handlers
    def handle_server_package(self, package):
        if package['type'] == 'message':
            print('{} >> {}'.format(
                package['sender_username'], package['data']))
        elif package['type'] == 'menu':
            print('{}\n'.format(package['data']))

    def monitor(self):
        readable_changes, _, _ = select([self.socket, stdin], [], [])
        for change in readable_changes:
            if change == self.socket:
                self.handle_server_package(self.parse_package(self.receive()))
            elif change == stdin:
                message = stdin.readline().strip()
                if message.startswith('/'):
                    self.command_handler(message)
                else:
                    self.send_message(message)

    def command_handler(self, command):    
        if command == '/commands':
            self.show_commands()
        elif command == '/rooms':
            self.list_rooms()
        elif command == '/join':
            self.join_room()
        elif command == '/create':
            room_name = input('Enter the room name: ')
            max_clients = input('Enter the max clients: ')
            self.create_room(room_name, max_clients)
        elif command == '/leave':
            self.leave_room()
        elif command == '/quit':
            print('Exiting app...')
            self.disconnect()
            exit(0)
        else:
             print(' * Command not found, please try again')