import socket

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
        self.connections.append((client, address))
        print(" * Connection recieved from {}:{}".format(address[0], address[1]))

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
