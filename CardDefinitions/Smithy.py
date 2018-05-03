from communication import read_message, send_input_command, send_print_command, send_end_command
from CardDefinitions.Card import Card
class Smithy(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Smithy"
        self.card_types = ['action']
        self.cost = 4
        self.text = """
        +3 Cards
        """
    def play(self,player):
        player.draw(number_to_draw=3)
        send_end_command(player.connection)

