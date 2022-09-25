from os import system, name

def clear_terminal():
    system('cls' if name == 'nt' else 'clear')
