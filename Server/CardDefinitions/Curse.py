from CardDefinitions.Card import Card
class Curse(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Curse"
        self.card_types = ['curse']
        self.cost = 0
        self.value = -1
        self.text = "-1 VP"
