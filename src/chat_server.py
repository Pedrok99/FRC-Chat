from time import sleep
from models.chat_server_model import Chat
from models.chat_room import Room
from utils.utils import clear_terminal

chat_manager = Chat(Room)

try: 
  while True:
    updates = chat_manager.monitor()
    print('>>')
    for client in updates:
      if client is chat_manager.socket:
        chat_manager.accept_connection()
      else:
        chat_manager.handle_client_request(client)
except KeyboardInterrupt:
  chat_manager.close()
