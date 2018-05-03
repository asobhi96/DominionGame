from CardDefinitions.Card import Card
from communication import read_message, send_input_command, send_print_command, send_end_command

class Market(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Market"
        self.card_types = ['action']
        self.cost = 5
        self.text = """
        +1 Card
        +1 Action
        +1 Buy
        +$1.
        """
    def play(self,player):
        player.draw()
        player.actions += 1
        player.buys += 1
        player.money += 1
        send_end_command(player.connection)

