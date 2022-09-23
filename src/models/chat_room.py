class Room:
    def __init__(self, id, name, max_clients=3):
        self.id = id
        self.name = name
        self.max_clients = max_clients
        self.clients = []

    def can_join(self):
        return len(self.clients) < self.max_clients

    def get_room_info(self):
        return "{} - {}: {} / {}".format(self.id, self.name, len(self.clients), self.max_clients)

    def add_client(self, client):
        self.clients.append(client)
        
