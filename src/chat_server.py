from models.tcp_server import Server

chat = Server()

chat.create()

chat.listen()

chat.accept_connection()

print(chat.get_message(chat.connections[0][0]))

chat.send_message(chat.connections[0][0], 'Hello, im a server')

chat.close()
