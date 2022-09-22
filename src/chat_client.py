from models.tcp_client import Client

chat_client = Client('localhost', 2222)

chat_client.connect()

chat_client.send('Hello, im a client')

print(chat_client.receive())

chat_client.close()