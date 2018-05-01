from CardDefinitions.Card import Card
class Workshop(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Workshop"
        self.card_types = ['action']
        self.cost = 3
        self.text = """
        Gain a card costing up to $4
        """
    def play(self,player):
        possible_cards = [card for card in player.supply.get_potential_purchases(max_cost=4)]
        for card in possible_cards:
            print(card)
        card = player.select_card_from_supply(max_cost=4)
        player.gain_card(card.card_name)
