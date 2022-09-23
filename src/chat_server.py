from time import sleep
from models.chat_server_model import Chat
from models.chat_room import Room
from utils.utils import clear_terminal

lastRoomId = 0

rooms = {}

chat_manager = Chat()

rooms[lastRoomId] = Room(lastRoomId, 'Main Lobby', max_clients=99)
lastRoomId += 1

while True:
  #clear_terminal()
  print(chat_manager.build_menu(rooms))
  updates = chat_manager.monitor()
  
  for client in updates:
    if client is chat_manager.socket:
      rooms = chat_manager.handle_new_client(rooms)
    else:
      print('Recieved message from {}: {}'.format(client.getpeername(), chat_manager.get_message(client)))

  sleep(2)
chat_manager.close()


