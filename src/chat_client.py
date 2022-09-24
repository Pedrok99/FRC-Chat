from time import sleep
from models.chat_client_model import ChatClient

chat_client = ChatClient('localhost', 2222)

chat_client.configure_client('Papuk')

menu = chat_client.wait_for_response()['data'] # Wait for the menu to be sent

print(menu)

chat_client.join_room()
 
# while True:
#   sleep(5)
#   print('Sending message in 5 seconds')
#   chat_client.send('Hi, im {}'.format(chat_client.socket.getsockname()))

sleep(5)

print('Disconnecting in 5 seconds')

chat_client.disconnect()