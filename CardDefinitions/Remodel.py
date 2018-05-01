from CardDefinitions.Card import Card
class Remodel(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Remodel"
        self.card_types = ['action']
        self.cost = 4
        self.text = """
        Trash a card from your hand. Gain a card costing up to $2 more than the trashed card.
        """
    def play(self,player):
        player.show_hand()
        print("Choose a card to trash")
        card = player.select_card_from_hand()
        original_cost = card.cost
        player.trash_from_hand(card)
        print("Choose a card to gain up to +2 trashed card cost")
        new_card = player.select_card_from_supply(max_cost=original_cost+2)
        print("Gaining a {}\n".format(new_card))
        player.gain_card(new_card.card_name.lower())
