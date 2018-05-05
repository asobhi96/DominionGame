import os
import socket
import supply
import player
from communication import read_message, send_print_command, print_and_send_command, send_kill_command
class GameServer():
    def __init__(self,board,number_of_players):
        self.supply = supply.Supply(configure_board=board)
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates a TCP socket
        self.players = []
        self.current_player = None
        self.current_player_id = 0
        self.current_connection = None
        self.number_of_players = number_of_players
        self.phase = None

    def connect_to_players(self):
        print("Waiting for player")
        self.server_socket.bind(("0.0.0.0",1025))
        self.server_socket.listen(self.number_of_players)
        for i in range(self.number_of_players):
            conn,addr = self.server_socket.accept()
            print("connection found")
            new_player = player.Player(name=read_message(connection=conn),id=i,game=self,connection=conn)
            send_print_command("Connected...waiting on other players")
            self.players.append(new_player)

    def set_up(self):
        self.connect_to_players()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        for player in self.players:
            player.add_to_deck("Copper",7)
            player.add_to_deck("Estate",3)
            player.shuffle_deck()
            player.draw(5)

    def play_turn(self):
        self.phase = 'action'
        self.current_player = self.players[self.current_player_id]
        self.current_connection = self.current_player.connection
        self.log("Player {} begins his turn\n".format(self.current_player.name))
        while self.current_player == self.players[self.current_player_id]:
            action = print_and_send_command(self.show_menu(),self.current_connection)
            if action == 'stats':
                self.stats()
            elif action == 'hand':
                self.hand()
            elif action == 'supply':
                self.get_supply()
            elif action == 'examine':
                self.examine()
            elif action == 'play':
                self.play_action()
            elif action == 'buy':
                self.buy_card()
            elif action == "end":
                self.end_turn()
            elif action == 'exit':
                self.exit_game()
            else:
                send_print_command("Invalid action",self.current_connection)

    def examine(self):
        card_name = print_and_send_command(self.supply.show_cards(),self.current_connection)
        card = self.supply.get_card(card_name)
        if card:
            send_print_command(str(card),self.current_connection)

    def get_supply(self):
        supply_string = self.supply.show_supply()
        send_print_command(supply_string,self.current_connection)

    def hand(self):
        send_print_command(self.current_player.show_hand(),self.current_connection)

    def stats(self):
        send_print_command(str(self.current_player),self.current_connection)

    def buy_card(self):
        if self.current_player.buys < 1:
            send_print_command("out of buys",self.current_connection)
        else:
            potential_buys = self.current_player.supply.get_potential_purchases(card_type='action')
            requested_card = print_and_send_command(potential_buys,self.current_connection).lower()
            card = self.supply.get_card(requested_card)
            if card and card.card_name.lower() in potential_buys:
                send_print_command(str(card),self.current_connection)
                confirmation = print_and_send_command("Enter yes to confirm purchase",self.current_connection)
                if confirmation == 'yes':
                    self.current_player.buy(card)
                    self.phase = 'buy'
                    self.log("Player {} bought {}\n".format(self.current_player.name,card.card_name))

    def play_action(self):
        if self.current_player.actions < 1 or not self.current_player.action_in_hand() or self.phase == 'buy':
            send_print_command("cannot play action cards",self.current_connection)
        else:
            playable_cards = self.current_player.show_hand(card_type='action')
            requested_card = print_and_send_command(playable_cards,self.current_connection)
            card = self.supply.get_card(requested_card)
            if card and card.card_name in playable_cards:
                send_print_command(str(card),self.current_connection)
                confirmation = print_and_send_command("Do you want to play this card?",self.current_connection)
                if confirmation == 'yes':
                    self.current_player.play_card(card)
                    self.log("Player {} played {}\n".format(self.current_player.name,card.card_name))

    def opponents_of(self,player):
        return [opponent for opponent in self.players if opponent != player]

    def main_loop(self):
        self.set_up()
        while not self.is_game_over():
            self.play_turn()
        print("Game over")

    def is_game_over(self):
        if self.supply.count_empty_piles() >= 3:
            return True
        return False

    def exit_game(self):
        for player in self.players:
            send_kill_command(player.connection)
            player.connection.close()
        exit()

    def end_turn(self):
        self.current_player.clean_up()
        self.phase = 'clean_up'
        self.log("Player {} ends their turn\n".format(self.current_player.name))
        self.current_player_id = self.current_player_id + 1 % len(self.players)

    def show_menu(self):
        return """
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
    def log(self,message):
        print(message)
        for player in self.players:
            send_print_command(message,player.connection)

def main():
    with open("card_config.txt",'r') as f:
        configure = []
        for card in f:
            name,supply = card.strip().split(',')
            configure.append(tuple([name,int(supply)]))
        number_of_players = int(input("Enter # of players\n"))
        game = GameServer(board=configure,number_of_players=number_of_players)
        game.main_loop()

if __name__ == "__main__":
    main()
