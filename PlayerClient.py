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
            os.system('cls')
            self.process_action(action)

    def choose_action(self):
        self.show_menu()
        action = input("Enter action\n")
        while action not in ['hand','supply','stats','examine','buy','play','end','exit']:
            action = input("Enter action\n")
        return action

    def show_menu(self):
        print("""
            It is your turn

            Enter 'hand' to view your hand
            Enter 'supply' to view the supply
            Enter 'examine' to look at a card
            Enter 'stats' to see your current stats
            Enter 'play' to play a card
            Enter 'buy' to purhcase a card
            Enter 'end' to end your turn
            Enter 'exit'to exit the game

            """
        )
    def process_action(self,action):
        if action == 'hand':
            self.show_hand()
        elif action == 'supply':
            self.show_supply()
        elif action == 'stats':
            self.show_stats()
        elif action == 'buy':
            self.buy_card()
        elif action == 'examine':
            self.examine_card()
        elif action == 'play':
            self.play_card()
        elif action == 'end':
            self.end_turn()
        elif action == 'exit':
            self.exit_game()

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

    def examine_card(self):
        send_message('examine',self.connection)
        supply = read_message(self.connection)
        print(supply)
        request = input("Enter the card you wish to examine\n").lower()
        while request not in supply:
            request = input("Enter the card you wish to examine\n").lower()
        send_message(request,self.connection)
        print(read_message(self.connection))
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

    def play_card(self):
        send_message('play',self.connection)
        if read_ack(self.connection):
            potential_actions = read_message(self.connection)
            print(potential_actions)
            request = input("Enter card you wish to play\n").capitalize()
            while request not in potential_actions:
                request = input("Enter card you wish to play\n")
            send_message(request,self.connection)
            print(read_message(self.connection))
            confirmation = input("Enter yes to play card\n")
            if confirmation == 'yes':
                print("Card played")
            else:
                print("Card not played")
            send_message(confirmation,self.connection)
        else:
            print("Out of actions")
        send_ack(self.connection)

    def end_turn(self):
        send_message('end',self.connection)

    def exit_game(self):
        send_message('exit',self.connection)
        self.connection.close()
        exit()




def main():
    player = PlayerClient()
    player.play()
if __name__ == "__main__":
    main()
