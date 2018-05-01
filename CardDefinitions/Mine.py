from CardDefinitions.Card import Card
class Mine(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Mine"
        self.card_types = ['action']
        self.cost = 5
        self.text = """
        You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to $3 more than it.
        """
    def play(self,player):
        player.show_hand()
        print("Choose a card to trash")
        treasure = player.select_card_from_hand(card_type = 'treasure')
        original_cost = treasure.cost
        player.trash_from_hand(treasure)
        print("Choose a card to gain up to +3 trashed card cost")
        treasure_card = player.select_card_from_supply(card_type = 'treasure',max_cost=original_cost+3)
        print("Gaining a {}\n".format(treasure_card))
        player.gain_card(treasure_card.card_name.lower())
