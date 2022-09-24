
from models.chat_client_model import ChatClient

chat_client = ChatClient('localhost', 2222)

chat_client.configure_client(input('Enter your username: '))

menu = chat_client.wait_for_response()['data'] # Wait for the menu to be sent

print(menu)

chat_client.join_room()


try:
  while True:
   chat_client.monitor()
  
except KeyboardInterrupt:
  print('Disconnecting...')
  chat_client.disconnect()
