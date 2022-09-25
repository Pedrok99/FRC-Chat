import socket
from select import select
from json import dumps, loads

from models.chat_room import Room

class Server:
    def __init__(self, ip='localhost', port=2222, max_connections=5, buffer_size=1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.max_connections = max_connections
        self.connections = []

    def create(self):
        """Create a socket and bind it to the specified IP and port"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            print(" * Bound to {}:{}".format(self.ip, self.port))

        except socket.error as msg:
            print(" * Error: {}".format(msg))
            self.socket.close()
            exit(1)

    def listen(self):
        """Listen for incoming connections"""
        try:
            self.socket.listen(self.max_connections)
            print(" * Server is now ready to recieve connections. (max connections: {})".format(self.max_connections))
        except socket.error as msg:
            print(" * Error: {}".format(msg))

    def accept_connection(self):
        """Handle a single incoming connection"""
        client, address = self.socket.accept()
        self.connections.append(client)
        print(
            " * Succefully connected to {}:{}".format(address[0], address[1]))
        return client

    def get_message(self, client):
        """Read a message from a client"""
        return client.recv(self.buffer_size).decode()

    def send_message(self, client, message):
        """Encode and Send a message to a client"""
        client.send(message.encode())

    def close(self):
        """Closes the socket"""
        print(" * Shutting down server...")
        self.socket.close()
        print(" * Server is now closed")


class Chat (Server):
    def __init__(self, Room_class, ip='localhost', port=2222, max_connections=5, buffer_size=1024 ):
        super().__init__(ip, port, max_connections, buffer_size)
        self.id = '{}:{}'.format(self.ip, self.port)
        self.number_of_rooms = 0
        self.rooms = {}
        self.Room_class = Room_class
        self.rooms[str(self.number_of_rooms)] = Room_class(str(self.number_of_rooms), 'Main Lobby', max_clients=99)
        # Init the server
        self.create()
        self.listen()

    def get_new_room_id(self):
        """Get a new room id"""
        self.number_of_rooms += 1
        return str(self.number_of_rooms)
    
    def create_package(self, type, data, sender_id, sender_username):
        """Create a package package
        Ex: {type: 'message', sender_id: 'ip:port', data: 'Hello world!}
        """
        package = {
            'type': type,
            'data': data,
            'sender_id': sender_id,
            'sender_username': sender_username
        }
        return dumps(package)

    def parse_package(self, package):
        """Parse a package from a client
        Ex: {type: 'message', sender_id: 'ip:port', data: 'Hello world!, target_room_id: Number || None}
        """
        print('parsing package: {}'.format(package))
        return loads(package)
    
    def send_room_message(self, sender, room, package):
        for client in room.clients:
            if client != sender:
                client.send(dumps(package).encode())

    def build_menu(self):
        menu = """Chat rooms:\n{}""".format(
            ''.join([str(room.get_room_status())+'\n' for room in self.rooms.values()]))
        return menu

    def monitor(self):
        readable_changes, _, _ = select(
            self.connections + [self.socket], [], [])
        return readable_changes

    # request handlers
    
    def handle_user_message(self, client, package):
        """Handle a user message to a chat room"""
        target_room = self.rooms[package['target_room_id']]
        self.send_room_message(client, target_room, package)
        
    def handle_user_list_rooms(self, client, package):
        """Handle a user request to list all chat rooms"""
        menu = self.build_menu()
        package = self.create_package('menu', menu, self.id, 'Server')
        self.send_message(client, package)
    
    def handle_user_room_info(self, client, package):
        """Handle a user request for listing room info"""
        target_room = self.rooms[package['target_room_id']]
        package = self.create_package('room_info', target_room.get_room_users(), self.id, 'Server')
        self.send_message(client, package)
            
    def handle_client_request(self, client): 
        package = self.parse_package(client.recv(self.buffer_size).decode())
        
        if package['type'] == 'message':
            self.handle_user_message(client, package)
            
        elif package['type'] == 'list_rooms':
            self.handle_user_list_rooms(client, package)
            
        elif package['type'] == 'room_info':
            self.handle_user_room_info(client, package)
            
        elif package['type'] == 'join_room':
            print(' * Client {} wants to join room: {}'.format(package['sender_username'], package['target_room_id']))
            target_room_id = package['target_room_id']
            username = package['sender_username']
            sender_id = package['sender_id']
            if target_room_id in self.rooms:
                if(self.rooms[target_room_id].can_join()):
                    self.rooms[target_room_id].add_client(client, {'username': username, 'id': sender_id})
                    print(' * Client {} ({}) has joined room: {}'.format(username, sender_id, target_room_id))
                    client.send('ok'.encode())
                else:
                    print(' * Ops :0. Looks like there is not enough space for you there :('.format(username, sender_id, target_room_id))
                    client.send('Could not join room: {}'.format(target_room_id).encode())
            else:
                print(' * Room {} does not exist'.format(target_room_id))
                client.send(' * Room {} does not exist'.format(target_room_id).encode())
                
        elif package['type'] == 'leave_room':
            print(' * Client {} wants to leave room: {}'.format(package['sender_username'], package['target_room_id']))
            target_room_id = package['target_room_id']
            username = package['sender_username']
            sender_id = package['sender_id']

            if target_room_id in self.rooms:
                self.rooms[target_room_id].remove_client(client)
                print(' * Client {} ({}) has left room: {}'.format(username, sender_id, target_room_id))
            else:
                print(' * Room {} does not exist'.format(target_room_id))
              
        elif package['type'] == 'create_room':
            room_name = package['data']['room_name']
            room_limit = int(package['data']['limit'])
            new_room_id = self.get_new_room_id()
            self.rooms[new_room_id] = Room(new_room_id, room_name, room_limit)
        
        elif package['type'] == 'disconnect':
            print(' * {} pistolou e kitou. Tinha que ser careca :( '.format(package['sender_username']))
            self.connections.remove(client)
            if package['target_room_id'] in self.rooms:
                self.rooms[package['target_room_id']].remove_client(client)
            client.close()

