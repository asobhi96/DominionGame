from CardDefinitions.Card import Card
class Village(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Village"
        self.card_types = ['action']
        self.cost = 3
        self.text = """
        +1 Cards
        +2 Actions
        """
    def play(self,player):
        player.draw(number_to_draw=1)
        player.actions += 2
