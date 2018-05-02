import os
import socket
import Supply
import Player
from communication import read_message, read_ack, send_message, send_ack
class GameServer():
    def __init__(self,board,number_of_players):
        self.supply = Supply.Supply(configure_board=board)
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates a TCP socket
        self.client_sockets = []
        self.players = []
        self.current_player = 0
        self.number_of_players = number_of_players
        self.phase = 'action'

    def connect_to_players(self):
        self.server_socket.bind(("0.0.0.0",1025))
        self.server_socket.listen(self.number_of_players)
        for i in range(self.number_of_players):
            conn,addr = self.server_socket.accept()
            print("connection found")
            self.client_sockets.append(conn)
            player = Player.Player(name=read_message(connection=conn),id=i,game=self)
            self.players.append(player)

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
        action = "start"
        while action != "end":
            action = self.prompt()
            if action == 'stats':
                self.stats()
            elif action == 'hand':
                self.hand()
            elif action == 'supply':
                self.get_supply()
            elif action == 'play' and self.phase == 'action':
                self.play_action()
            elif action == 'buy':
                self.buy_card()
                self.phase = 'buy'
            elif action == "end":
                self.end()
                self.phase = 'clean_up'
                player.clean_up()
            elif action == 'exit':
                self.exit()
            elif action == 'examine':
                self.examine()

    def get_supply(self):
        player,connection = self.get_player_and_client()
        supply_string = self.supply.show_supply()
        send_message(supply_string,connection)
        ack = read_ack(connection)

    def hand(self):
        player,connection = self.get_player_and_client()
        send_message(player.show_hand(),connection)
        ack = read_ack(connection)

    def stats(self):
        player, connection = self.get_player_and_client()
        send_message(str(player),connection)
        ack = read_ack(connection)

    def buy_card(self):
        player,connection = self.get_player_and_client()
        if player.buys < 1:
            send_message("out of buys",connection)
        else:
            send_ack(connection)
            send_message(self.supply.get_potential_purchases(player.calculate_money()),connection)
            requested_card = read_message(connection)
            card = self.supply.create_card_from_supply(requested_card)
            send_message(str(card),connection)
            confirmation = read_message(connection)
            if confirmation == 'yes':
                player.buy(card)
        ack = read_ack(connection)

    def opponents_of(self,player):
        return [opponent for opponent in self.players if opponent != player]

    def prompt(self):
        player, connection = self.get_player_and_client()
        print("Sending menu to player")
        send_message("menu",connection)
        return read_message(connection)

    def main_loop(self):
        self.set_up()
        while not self.is_game_over():
            self.play_turn()
        print("Game over")

    def is_game_over(self):
        if self.supply.count_empty_piles() >= 3:
            return True
        return False

    def get_player_and_client(self):
        return self.players[self.current_player],self.client_sockets[self.current_player]

def main():
    with open("card_config.txt",'r') as f:
        configure = []
        for card in f:
            name,cost,supply = card.strip().split(',')
            configure.append(tuple([name,int(cost),int(supply)]))
        game = GameServer(board=configure,number_of_players=1)
        game.main_loop()

if __name__ == "__main__":
    main()
