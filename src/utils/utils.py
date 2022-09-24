from os import system, name

def clear_terminal():
    system('cls' if name == 'nt' else 'clear')
    
def show_commands():
    print('Commands:')
    print('  /commands - show this command screen')
    print('  /rooms - show available rooms')
    print('  /join <room_id> - join a room')
    print('  /leave - leave the current room')
    print('  /quit - quit the chat app')