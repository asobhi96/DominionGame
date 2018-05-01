from CardDefinitions.Card import Card
class Copper(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Copper"
        self.card_types = ['treasure']
        self.cost = 0
        self.value = 1
        self.text = "$1"
