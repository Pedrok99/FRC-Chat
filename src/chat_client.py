from time import sleep
from models.chat_client_model import ChatClient

chat_client = ChatClient('localhost', 2222)

menu = chat_client.wait_for_response()['data'] # Wait for the menu to be sent

print(menu)



# selected_room = input('Enter the desired room: ')
# print('selected room: {}'.format(selected_room))
# chat_client.send(selected_room)
# 
# while True:
#   sleep(5)
#   print('Sending message in 5 seconds')
#   chat_client.send('Hi, im {}'.format(chat_client.socket.getsockname()))


chat_client.close()