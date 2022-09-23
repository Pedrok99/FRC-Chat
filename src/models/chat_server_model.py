import socket
from select import select
from json import dumps, loads


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
        """Recieve a message from a client"""
        return client.recv(self.buffer_size).decode()

    def send_message(self, client, message):
        """Send a message to a client"""
        client.send(message.encode())

    def close(self):
        """Closes the socket"""
        print(" * Shutting down server...")
        self.socket.close()
        print(" * Server is now closed")


class Chat (Server):
    def __init__(self, ip='localhost', port=2222, max_connections=5, buffer_size=1024):
        super().__init__(ip, port, max_connections, buffer_size)
        self.id = '{}:{}'.format(self.ip, self.port)
        self.create()
        self.listen()

    def create_package(self, type, data, sender_id):
        """Create a package package
        Ex: {type: 'message', sender_id: 'ip:port', data: 'Hello world!}
        """
        package = {
            'type': type,
            'data': data,
            'sender_id': sender_id,
        }
        return dumps(package)

    def parse_package(self, package):
        """Parse a package from a client
        Ex: {type: 'message', sender_id: 'ip:port', data: 'Hello world!, target_room_id: 1 || None}
        """
        return loads(package)
    
    def build_menu(self, rooms):
        menu = """Chat rooms:\n\n{}""".format(
            ''.join([str(room.get_room_info()) for room in rooms.values()]))
        return menu

    def handle_new_client(self, rooms):
        new_client = self.accept_connection()
        menu = self.build_menu(rooms)
        package = self.create_package('menu', menu, self.id)
        new_client.send(package.encode())  # send menu to new client


#        target_room_id = new_client.recv(self.buffer_size).decode()
#        print('client {} wants to join room: {}'.format(new_client.getpeername(), target_room_id))
#        target_room_id = int(target_room_id)
#        if target_room_id in rooms:
#            rooms[target_room_id].add_client(new_client)
#            print('client {} has joined room: {}'.format(new_client.getpeername(), target_room_id))
#
#        else:
#            print('room {} does not exist'.format(target_room_id))
        return rooms

    def monitor(self):
        readable_changes, _, _ = select(
            self.connections + [self.socket], [], [])
        return readable_changes

