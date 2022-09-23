from time import sleep
from models.chat_client_model import Client

chat_client = Client('localhost', 2222)

chat_client.connect()

print(chat_client.wait_for_response())


selected_room = input('Enter the desired room: ')
print('selected room: {}'.format(selected_room))
chat_client.send(selected_room)

while True:
  sleep(5)
  print('Sending message in 5 seconds')
  chat_client.send('Hi, im {}'.format(chat_client.socket.getsockname()))


chat_client.close()