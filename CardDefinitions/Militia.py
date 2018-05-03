from CardDefinitions.Card import Card
from communication import read_message, send_input_command, send_print_command, send_end_command
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
            #opponent.prompt_reaction()
            while len(opponent.hand) > 3 and not opponent.is_safe:
                send_print_command(opponent.show_hand(),opponent.connection)
                send_print_command("Choose a card to discard from your hand",opponent.connection)
                card_name = read_message(opponent.connection).lower()
                card = opponent.find_card_from_hand(opponent.connection)
                if card:
                    opponent.discard_from_hand(card)
                    break
            send_end_command(opponent.connection)
        send_end_command(player.connection)
