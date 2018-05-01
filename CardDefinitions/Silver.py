from CardDefinitions.Card import Card
class Silver(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Silver"
        self.card_types = ['treasure']
        self.cost = 3
        self.value = 2
