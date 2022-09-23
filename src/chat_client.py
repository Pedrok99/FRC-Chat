from time import sleep
from models.tcp_client import Client

chat_client = Client('localhost', 2222)

chat_client.connect()

while True:
  print('Sending message in 5 seconds')
  sleep(5)
  chat_client.send('Hi, im {}'.format(chat_client.socket.getsockname()))
   


chat_client.close()