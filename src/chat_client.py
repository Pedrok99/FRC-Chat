
from models.chat_client_model import ChatClient
from utils.utils import clear_terminal, show_commands

chat_client = ChatClient('localhost', 2222)

chat_client.configure_client(input('Enter your username: '))

clear_terminal()

chat_client.show_commands()



#chat_client.join_room()



try:
  while True:
   chat_client.monitor()
  
except KeyboardInterrupt:
  print('Disconnecting...')
  chat_client.disconnect()
