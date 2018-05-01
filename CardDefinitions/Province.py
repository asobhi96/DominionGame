from CardDefinitions.Card import Card
class Province(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Province"
        self.card_types = ['victory']
        self.cost = 8
        self.victory_points = 6
