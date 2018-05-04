import os
import socket
import supply
import player
from communication import read_message, read_ack, send_message, send_ack, send_print_command, send_end_command
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
        self.server_socket.bind(("0.0.0.0",1025))
        self.server_socket.listen(self.number_of_players)
        for i in range(self.number_of_players):
            conn,addr = self.server_socket.accept()
            print("connection found")
            new_player = player.Player(name=read_message(connection=conn),id=i,game=self,connection=conn)
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
        action = "start"
        while action != "end":
            action = self.prompt_player()
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

    def request_card(self,card_type=None,max_cost=100):
        send_message(self.supply.get_potential_purchases(card_type=card_type,max_cost=max_cost),self.current_connection)
        requested_card = read_message(self.current_connection)
        return self.supply.get_card(requested_card)


    def examine(self):
        card = self.request_card()
        send_message(str(card),self.current_connection)
        ack = read_ack(self.current_connection)

    def get_supply(self):
        supply_string = self.supply.show_supply()
        send_message(supply_string,self.current_connection)
        ack = read_ack(self.current_connection)

    def hand(self):
        send_message(self.current_player.show_hand(),self.current_connection)
        ack = read_ack(self.current_connection)

    def stats(self):
        send_message(str(self.current_player),self.current_connection)
        ack = read_ack(self.current_connection)

    def buy_card(self):
        if self.current_player.buys < 1:
            send_message("out of buys",self.current_connection)
        else:
            send_ack(self.current_connection)
            card = self.request_card(max_cost=self.current_player.calculate_money())
            send_message(str(card),self.current_connection)
            confirmation = read_message(self.current_connection)
            if confirmation == 'yes':
                self.current_player.buy(card)
                self.phase = 'buy'
        ack = read_ack(self.current_connection)

    def play_action(self):
        if self.current_player.actions < 1 or not self.current_player.action_in_hand() or self.phase == 'buy':
            send_message("cannot play action cards",self.current_connection)
        else:
            send_ack(self.current_connection)
            send_message(self.current_player.show_hand(card_type='action'),self.current_connection)
            requested_action = read_message(self.current_connection)
            card = self.supply.get_card(requested_action)
            send_message(str(card),self.current_connection)
            confirmation = read_message(self.current_connection)
            if confirmation == 'yes':
                self.current_player.play_card(card)
        ack = read_ack(self.current_connection)


    def log(self,message):
        for player in self.players:
            send_message("command_mode",player.connection)
            send_print_command(message,player.connection)
            send_end_command(player.connection)

    def opponents_of(self,player):
        return [opponent for opponent in self.players if opponent != player]

    def prompt_player(self):
        print("Sending menu to {}\n".format(self.current_player.name))
        send_message("menu",self.current_connection)
        return read_message(self.current_connection)

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
            player.connection.close()
        exit()

    def end_turn(self):
        self.current_player.clean_up()
        self.phase = 'clean_up'

def main():
    with open("card_config.txt",'r') as f:
        configure = []
        for card in f:
            name,supply = card.strip().split(',')
            configure.append(tuple([name,int(supply)]))
        game = GameServer(board=configure,number_of_players=1)
        game.main_loop()

if __name__ == "__main__":
    main()
