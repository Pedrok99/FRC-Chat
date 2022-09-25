class Room:
    def __init__(self, id, name, max_clients=3):
        self.id = id
        self.name = name
        self.max_clients = max_clients
        self.clients = []
        self.client_details = {} # key: client.fileno(), value: {username: 'username', id: 'id'}

    def can_join(self):
        return len(self.clients) < self.max_clients

    def get_room_status(self):
        return "{} - {}: {} / {}".format(self.id, self.name, len(self.clients), self.max_clients)

    def add_client(self, client, details):
        self.clients.append(client)
        self.client_details[client.fileno()] = details
        
    def remove_client(self, client):
        self.clients.remove(client)
        self.client_details.pop(client.fileno())
        
    def get_room_users(self):
        details =  self.client_details.values()
        users_details = [str(detail['username']) for detail in details]
        users_details ='Users connected to this room:\n\n'+'\n'.join(users_details)
        return users_details
