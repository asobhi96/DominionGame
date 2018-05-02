import os
import socket
import Supply
import Player
from communication import read_message, read_ack, send_message, send_ack

class PlayerClient():
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates a TCP socket
        self.connect_to_game_host()
        send_message('Arman',self.connection)

    def connect_to_game_host(self):
        self.connection.connect(('localhost',1025))

    def play(self):
        while True:
            menu = read_message(self.connection)
            action = self.choose_action()
            self.process_action(action)

    def choose_action(self):
        action = input("Enter action\n")
        while action not in ['hand','supply','stats','buy']:
            action = input("Enter action\n")
        return action

    def process_action(self,action):
        if action == 'hand':
            self.show_hand()
        elif action == 'supply':
            self.show_supply()
        elif action == 'stats':
            self.show_stats()
        elif action == 'buy':
            self.buy_card()

    def show_hand(self):
        send_message('hand',self.connection)
        hand = read_message(self.connection)
        print(hand)
        send_ack(self.connection)

    def show_supply(self):
        send_message('supply',self.connection)
        supply = read_message(self.connection)
        print(supply)
        send_ack(self.connection)

    def show_stats(self):
        send_message('stats',self.connection)
        stats = read_message(self.connection)
        print(stats)
        send_ack(self.connection)

    def buy_card(self):
        send_message('buy',self.connection)
        if read_ack(self.connection):
            potential_buys = read_message(self.connection)
            print(potential_buys)
            request = input("Enter card you wish to buy\n").lower()
            while request not in potential_buys:
                request = input("Enter card you wish to buy\n")
            send_message(request,self.connection)
            print(read_message(self.connection))
            confirmation = input("Enter yes to purchase card\n")
            if confirmation == 'yes':
                print("Card purchased")
            else:
                print("Card not purchased")
            send_message(confirmation,self.connection)
        else:
            print("Out of buys")
        send_ack(self.connection)




def main():
    player = PlayerClient()
    player.play()
if __name__ == "__main__":
    main()
