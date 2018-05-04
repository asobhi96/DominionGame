from CardDefinitions.Card import Card
class Duchy(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Duchy"
        self.card_types = ['victory']
        self.cost = 5
        self.victory_points = 3
        self.text = "3 VP"
