from time import sleep
from models.tcp_server import Server
from select import select

lastRoomId = 0

rooms = {}

chat = Server()
chat.create()
chat.listen()

while True:
  readable_changes, _, _= select( chat.connections + [chat.socket], [] , [])
  print('-' * 20)
  for client in readable_changes:
    if client is chat.socket:
      chat.accept_connection()
    else:
      print('Recieved message from {}: {}'.format(client.getpeername(), chat.get_message(client)))

  sleep(2)
chat.close()
