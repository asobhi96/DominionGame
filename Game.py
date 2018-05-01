import Supply
import Player
class Game():
    def __init__(self,board,number_of_players):
        self.supply = Supply.Supply(configure_board=board)
        self.players = []
        for player_id in range(number_of_players):
            self.players.append(Player.Player(name='test',id=player_id,game=self))
        self.current_player = 0

    def set_up(self):
        for player in self.players:
            player.add_to_deck("Copper",7)
            player.add_to_deck("Estate",3)
            player.shuffle_deck()
            player.draw(5)


    def play_turn(self):
        player = self.players[self.current_player]
        print("player {}'s turn".format(self.current_player))
        action = "start"
        while action != "end":
            self.prompt()
            action = input("choose an action\n").lower()
            if action == 'stats':
                print(player)
            elif action == 'hand':
                player.show_hand()
            elif action == 'supply':
                self.supply.show_supply()
            elif action == 'money':
                print("Player has ${}\n".format(player.calculate_money()))
            elif action == 'play':
                player.choose_and_play_action()
            elif action == 'buy':
                if player.buy_card():
                    print("Card sucessfully purhcased")
                else:
                    print("Out of buys")
            elif action == "end":
                player.clean_up()
                self.current_player = (self.current_player + 1) % len(self.players)
            elif action == 'exit':
                exit()
            elif action == 'examine':
                for card in self.supply.card_list:
                    print(card)
                player.examine_card()

    def main_loop(self):
        self.set_up()
        while not self.is_game_over():
            self.play_turn()
        print("Game over")

    def is_game_over(self):
        if self.supply.count_empty_piles() >= 3:
            return True
        return False

    def opponents_of(self,player):
        return [opponent for opponent in self.players if opponent != player]

    def prompt(self):
        print('\n'*3)
        print("Enter 'hand' to view your hand")
        print("Enter 'stats' to view your current stats")
        print("Enter 'supply' to view the supply")
        print("Enter 'examine' to examine a card from the supply")
        print("Enter 'money' to see how much $ you have")
        print("Enter 'play' to play a card")
        print("Enter 'buy' to purhcase a card'")
        print("Enter 'end' to end your turn")
        print("Enter 'exit' to exit this game")
        print('\n'*3)
