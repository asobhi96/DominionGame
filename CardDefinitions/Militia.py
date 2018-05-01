from CardDefinitions.Card import Card
class Militia(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Militia"
        self.card_types = ['action','attack']
        self.cost = 4
        self.text = """
        +$2
        Each other player discards down to 3 cards in their hand.
        """
    def play(self,player):
        player.money += 2
        for opponent in player.game.opponents_of(player):
            opponent.prompt_reaction()
            while len(opponent.hand) > 3 and not opponent.is_safe:
                opponent.choose_card_to_discard()
