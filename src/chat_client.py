from time import sleep
from models.chat_client_model import ChatClient

chat_client = ChatClient('localhost', 2222)

chat_client.configure_client('Papuk')

menu = chat_client.wait_for_response()['data'] # Wait for the menu to be sent

print(menu)

chat_client.join_room()


try:
  while True:
   sleep(1)
   chat_client.send_message('Melhor que a entrega de vcs só a do alectron')
   # chat_client.monitor()
   
   print('>>')
  
except KeyboardInterrupt:
  print('Disconnecting...')
  chat_client.disconnect()
