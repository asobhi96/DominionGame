from communication import read_message, send_input_command, send_print_command, send_end_command
from CardDefinitions.Card import Card
class Woodcutter(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Woodcutter"
        self.card_types = ['action']
        self.cost = 3
        self.text = """
        +1 Buy
        +2 $
        """
    def play(self,player):
        player.buys += 1
        player.money += 2
        send_end_command(player.connection)
