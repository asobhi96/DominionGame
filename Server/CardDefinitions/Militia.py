from CardDefinitions.Card import Card
from communication import read_message, send_input_command, send_print_command
class Militia(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Militia"
        self.card_types = ['action','attack']
        self.cost = 4
        self.text = """
        +$2
        Each other player discards down to 3 cards in their hand.
        """
    def play(self,player):
        player.money += 2
        for opponent in player.game.opponents_of(player):
            for card in opponent.hand:
                if 'reaction' in card.card_types:
                    send_print_command("Player {} has played attack card {}\nEnter yes to react with {}\n".format(player.name,self.card_name,card.card_name),opponent.connection)
                    send_input_command(opponent.connection)
                    response = read_message(opponent.connection)
                    if response == 'yes':
                        send_print_command("Reacting with {}\n")
                        card.react(opponent)

            while len(opponent.hand) > 3 and not opponent.is_safe:
                send_print_command(opponent.show_hand(),opponent.connection)
                send_print_command("Choose a card to discard from your hand",opponent.connection)
                card_name = read_message(opponent.connection).lower()
                card = opponent.find_card_from_hand(opponent.connection)
                if card:
                    opponent.discard_from_hand(card)
