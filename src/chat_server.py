from time import sleep
from models.chat_server_model import Chat
from models.chat_room import Room
from utils.utils import clear_terminal

rooms = {}

chat_manager = Chat()

fixed_lobby_id = chat_manager.get_new_room_id()
rooms[fixed_lobby_id] = Room(fixed_lobby_id, 'Main Lobby', max_clients=99)

try: 
  while True:
    updates = chat_manager.monitor()
    print('>>')
    for client in updates:
      if client is chat_manager.socket:
        chat_manager.handle_new_client(rooms)
      else:
        chat_manager.handle_client_request(client, rooms)
except KeyboardInterrupt:
  chat_manager.close()
