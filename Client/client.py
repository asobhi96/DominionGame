import os
import socket
from communication import send_message, read_message, read_command

class PlayerClient():
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates a TCP socket
        self.connect_to_game_host()
        send_message('Arman',self.connection)

    def connect_to_game_host(self):
        ip = input()
        self.connection.connect((ip,1025))

    def play(self):
        self.process_commands()

    def process_commands(self):
        while True:
            action_code, message = read_command(self.connection)
            if action_code == '0':
                print(message)
            elif action_code == '1':
                response = input()
                send_message(response,self.connection)
            elif action_code == '2':
                self.connection.close()
                break

def main():
    player = PlayerClient()
    player.play()

if __name__ == "__main__":
    main()
