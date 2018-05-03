import os
import socket
from communication import send_message, send_ack, read_message, read_ack, read_command

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
            if menu == 'command_mode':
                self.process_commands()
            else:
                action = self.choose_action()
                os.system('cls')
                self.process_action(action)

    def choose_action(self):
        self.show_menu()
        action = input("Enter action\n")
        while action not in ['hand','supply','stats','examine','buy','play','end','exit',]:
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
        elif action == 'command_mode':
            self.process_commands()

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

    def choose_valid_card(self,card_list):
        request = input("Enter the card name\n").lower()
        while request not in card_list and request.capitalize() not in card_list:
            request = input("Enter the card name\n")
        return request

    def send_and_recieve_response(self,message):
        send_message(message,self.connection)
        return read_message(self.connection)

    def ask_confirmation(self):
        confirmation = input("Enter yes to select card\n")
        if confirmation == 'yes':
            return True
        else:
            return False

    def examine_card(self):
        send_message('examine',self.connection)
        supply = read_message(self.connection)
        print(supply)
        request = self.choose_valid_card(supply)
        print(self.send_and_recieve_response(request))
        send_ack(self.connection)

    def buy_card(self):
        send_message('buy',self.connection)
        if read_ack(self.connection):
            potential_buys = read_message(self.connection)
            print(potential_buys)
            request = self.choose_valid_card(potential_buys)
            print(self.send_and_recieve_response(request))
            confirmation = self.ask_confirmation()
            if confirmation:
                print("Card purchased")
                send_message('yes',self.connection)
            else:
                print("Card not purchased")
                send_message('no',self.connection)
        else:
            print("Out of buys")
        send_ack(self.connection)

    def play_card(self):
        send_message('play',self.connection)
        if read_ack(self.connection):
            potential_actions = read_message(self.connection)
            print(potential_actions)
            request = self.choose_valid_card(potential_actions)
            print(self.send_and_recieve_response(request))
            confirmation = self.ask_confirmation()
            if confirmation:
                send_message('yes',self.connection)
                print("Card played")
                self.process_commands()
            else:
                send_message('no',self.connection)
                print("Card not played")
        else:
            print("Cannot play actions")
        send_ack(self.connection)

    def process_commands(self):
        while True:
            action_code, message = read_command(self.connection)
            if action_code == '0':
                print(message)
            elif action_code == '1':
                response = input()
                send_message(response,self.connection)
            elif action_code == '2':
                break

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
