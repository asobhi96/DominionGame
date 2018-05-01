from CardDefinitions.Card import Card
class Cellar(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Cellar"
        self.card_types = ['action']
        self.cost = 2
        self.text = """
        +1 Action
        Discard any number of cards, then draw that many.
        """
    def play(self,player):
        player.actions += 1
        number_of_cards_to_discard = int(input(("How many cards do you wish to discard?")))
        while number_of_cards_to_discard > len(player.hand):
            number_of_cards_to_discard = int(input(("You only have {} cards.\nHow many cards do you wish to discard?\n".format(len(player.hand)))))
        for _ in range(number_of_cards_to_discard):
            player.choose_card_to_discard()
        player.draw(number_to_draw=number_of_cards_to_discard)
