from CardDefinitions.Card import Card
class Gold(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Gold"
        self.card_types = ['treasure']
        self.cost = 6
        self.value = 3
