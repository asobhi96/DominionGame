from CardDefinitions.Card import Card
from communication import send_print_command,print_and_send_command
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
        send_print_command("Waiting for players...",player.connection)
        for opponent in player.game.opponents_of(player):
            for card in opponent.hand:
                if 'reaction' in card.card_types:
                    response = print_and_send_command("Player {} has played attack card {}\nEnter 'yes' to react with {}\n".format(player.name,self.card_name,card.card_name),opponent.connection)
                    if response == 'yes':
                        player.game.log("Player {} reacts with {}\n".format(player.name,card.card_name))
                        card.react(opponent)

            while len(opponent.hand) > 3 and not opponent.is_safe:
                send_print_command(opponent.show_hand(),opponent.connection)
                card_name = print_and_send_command("Choose a card to discard from your hand",opponent.connection).lower()
                card = opponent.find_card_from_hand(card_name)
                if card:
                    player.game.log("Player {} discards {}\n".format(player.name,card.card_name))
                    opponent.discard_from_hand(card)
