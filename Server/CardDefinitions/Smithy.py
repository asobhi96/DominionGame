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

