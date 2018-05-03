from communication import read_message, send_input_command, send_print_command, send_end_command
from CardDefinitions.Card import Card
class Moat(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Moat"
        self.card_types = ['action','reaction']
        self.cost = 2
        self.text = """
        +2 Cards
        ---------------
        When another player plays an Attack card, you may first reveal this from your hand, to be unaffected by it.
        """
    def play(self,player):
        player.draw(number_to_draw=2)
        send_end_command(player.connection)

    def react(self,player):
        player.reveal(self.card_name)
        player.is_safe = True

