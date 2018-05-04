from CardDefinitions.Card import Card
class Estate(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Estate"
        self.card_types = ['victory']
        self.cost = 2
        self.victory_points = 1
        self.text = "1 VP"

